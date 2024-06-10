"""
Asyncio Crawler Support
"""

import asyncio
from asyncio.queues import Queue
from collections import deque
import queue
from itertools import chain
import hashlib
import random
import re
import os
import sys
import traceback
from typing import Dict, List, Any, Callable
import time
import types
import sqlite3

# from pprint import pformat
import yaml
import aiohttp


from agptools.helpers import best_of, expandpath, I, parse_uri, build_uri
from agptools.progress import Progress
from agptools.containers import (
    walk,
    myassign,
    rebuild,
    SEP,
    list_of,
    overlap,
    soft,
    build_paths,
)

# from agptools.calls import scall

from agptools.logs import logger
from syncmodels import __version__
from syncmodels.definitions import (
    BODY_KEY,
    KIND_KEY,
    METHOD_KEY,
    FUNC_KEY,
    MONOTONIC_KEY,
    CRAWLER_KEY,
    BOT_KEY,
    # MONOTONIC_SINCE,
    MONOTONIC_SINCE_KEY,
    MONOTONIC_SINCE_VALUE,
    REG_PRIVATE_KEY,
    REG_SPLIT_PATH,
    URI,
    DURI,
    JSON,
)
from syncmodels.http import (
    guess_content_type,
    ALL_JSON,
    CONTENT_TYPE,
    USER_AGENT,
    APPLICATION_JSON,
)
from syncmodels.storage import WaveStorage
from syncmodels.exceptions import NonRecoverable
from syncmodels.syncmodels import SyncModel, COPY
from .crud import parse_duri, DEFAULT_DATABASE, DEFAULT_NAMESPACE, tf


# from syncmodels.syncmodels import Transformer


from .helpers import analyze_url
from .context import iContext
from .requests import iResponse

# ---------------------------------------------------------
# Loggers
# ---------------------------------------------------------
log = logger(__name__)

DEFAULT = "__default__"
UNKNOWN = "__unknown__"

SINGLE = "single"  # single stream subtype element, not a list
REG_KIND = r"(?P<parent>[^-]*)(-(?P<sub>.*))?$"


# ---------------------------------------------------------
# Authenticator Helpers
# ---------------------------------------------------------
class iAuthenticator:
    "base interface for authenticators"
    AUTH = None  #  not logged

    async def authenticate(self, url, params):
        "resolve authentication (i.e 401/404/407 alike situations)"


# ---------------------------------------------------------
# SQL Bots
# ---------------------------------------------------------


def most_common(sample):
    stats = {}
    for value in sample:
        stats[value] = stats.get(value, 0) + 1

    stats = [(v, k) for k, v in stats.items()]
    stats.sort(reverse=True)
    return stats


class iSchema:

    MONOTONIC_CANDIDATES = [
        r"entity_ts",
        r"ts",
        r"timestamp",
        r"date",
    ]

    def guess_schema(self, names, data, **kw):
        """
        info
        ({'date': {'name': 'date',
                   'type': 'TEXT',
                   'notnull': 0,
                   'default': None,
                   'pk': 0,
                   'hidden': 0},
          'value': {'name': 'value',
                    'type': 'REAL',
                    'notnull': 0,
                    'default': None,
                    'pk': 0,
                    'hidden': 0}},
         [{'name': 'date',
           'type': 'TEXT',
           'notnull': 0,
           'default': None,
           'pk': 0,
           'hidden': 0},
          {'name': 'value',
           'type': 'REAL',
           'notnull': 0,
           'default': None,
           'pk': 0,
           'hidden': 0}],
         'date')

        """
        d_fields = {}
        for row in data:
            for i, value in enumerate(row):
                name = names[i]
                type_ = value.__class__
                d_fields.setdefault(name, []).append(type_)

        for key, sample in d_fields.items():
            d_fields[key] = most_common(sample)[0][1]

        types = [d_fields[key] for key in names]

        def best():
            for value in d_fields:
                for pattern in self.MONOTONIC_CANDIDATES:
                    if re.match(pattern, value):
                        return value

        monotonic_since_key = best()
        return names, types, d_fields, monotonic_since_key


class StructShema:
    def __init__(self, names, types, d_fields, monotonic_since_key, struct):
        self.names = names
        self.types = types
        self.d_fields = d_fields
        self.monotonic_since_key = monotonic_since_key
        self.struct = struct


class iSession(iContext, iSchema, iAuthenticator):
    "The base for all 3rd party session accessors"

    DEFAULT_METHOD = "get"

    RESPONSE_META = ["headers", "links", "real_url"]

    SESSION_FACTORY = {}
    CACHE = {}
    "some data to be cached and shared"

    @classmethod
    def register(cls, *patterns):
        for pattern in patterns:
            cls.SESSION_FACTORY[pattern] = cls

    def __init__(self, bot, **kw):
        self.bot = bot
        self.connection_pool = {}
        self.headers = {}
        self.context = kw

    def _schema(self, uri: DURI):
        return self.CACHE.get(uri["uri"], {}).get(uri[KIND_KEY])

    async def _create_connection(self, url, **kw):
        raise NotImplementedError()

    async def _process_response(self, response):
        def expand(value):
            iterator = getattr(value, "items", None)
            if iterator:
                value = {k: expand(v) for k, v in iterator()}
            return value

        meta = {
            k: expand(getattr(response, k, None))
            for k in self.RESPONSE_META
            if hasattr(response, k)
        }
        content_type = guess_content_type(meta.get("headers", {}))
        if content_type == APPLICATION_JSON:
            stream = await response.json()
        else:
            stream = await response.text()
            assert isinstance(stream, str)
            # stream = [{'data': block} for block in stream.splitlines()]
            stream = [{"result": stream}]

        return stream, meta

    def _get_connection_key(self, uri: DURI):
        namespace = tf(uri.get("fscheme", DEFAULT_NAMESPACE))
        database = tf(uri.get("host", DEFAULT_DATABASE))
        key = namespace, database
        return key

    async def _get_connection(self, uri: DURI, **kw):
        key = self._get_connection_key(uri)
        connection = self.connection_pool.get(
            key
        ) or await self._create_connection(uri)
        return connection

    @classmethod
    async def new(cls, url, bot, **context):
        def score(item):
            "score by counting how many uri values are not None"
            uri, factory, m = item
            sc = 10 * len(m.groups()) + len(
                [_ for _ in uri.values() if _ is not None]
            )
            # sc = len(m.groups())
            return sc, (uri, factory)

        results = []
        uri = parse_uri(url)
        for pattern, factory in cls.SESSION_FACTORY.items():
            # TODO: extend to get more field from url
            # m = re.match(pattern, uri["fscheme"])
            m = re.match(pattern, url)
            if m:
                d = m.groupdict()
                soft(uri, d)
                results.append((uri, factory, m))

        if results:
            score, (uri, factory) = best_of(results, score)
            return factory(**uri, bot=bot, **context)
        raise RuntimeError(f"Unable to find iSession for {url}")

    async def get(self, url, headers=None, params=None, **kw) -> iResponse:
        "Note: Returns is not properly a iResponse, but we mimic the same interface"
        headers = headers or {}
        params = params or {}
        connection = await self._get_connection(
            url, **headers, **params, **kw
        )
        return await connection.get(
            url, headers=headers, params=params, **kw
        )

    async def _get_schema(self, _uri: DURI):
        uri = _uri["uri"]
        kind = _uri[KIND_KEY]
        info = self.CACHE.setdefault(uri, {})[kind] = (
            await self._inspect_schema(_uri)
        )
        return info

    async def _inspect_schema(self, _uri: DURI) -> StructShema:
        """performs an instrospection to figure-out the schema
        for a particular kind object
        """
        raise NotImplementedError()
        # fields = []
        # d_fields = {}
        # monotonic_since_key = None
        # return d_fields, fields, monotonic_since_key

    async def update_params(self, url, params, context):
        "last chance to modify params based on context for a specific iSession type"
        wave0 = context.get(MONOTONIC_KEY, None)
        if wave0:
            _uri = parse_uri(url, **context)
            schema = self._schema(_uri) or await self._get_schema(_uri)
            monotonic_since_key = schema.monotonic_since_key
            if monotonic_since_key in wave0:
                params[MONOTONIC_SINCE_KEY] = monotonic_since_key
                params[MONOTONIC_SINCE_VALUE] = wave0[monotonic_since_key]
            else:
                log.warning(
                    "MONOTONIC_SINCE_KEY [%s] is missing in wave: %s",
                    monotonic_since_key,
                    wave0,
                )
        call_kw = {
            "url": url,
            "headers": self.headers,
        }
        if context.get(METHOD_KEY, "get").lower() in ("post", "put"):
            if body := context.get(BODY_KEY):
                call_kw["json"] = body
        else:
            call_kw["params"] = params
        return call_kw


# ---------------------------------------------------------
# Agent
# ---------------------------------------------------------
class iAgent:
    "the minimal interface for an agent in crawler module"

    @classmethod
    def clean(cls):
        "clean shared (classmethod) data"

    def __init__(
        self,
        config_path=None,
        name="",
        include=None,
        exclude=None,
        *arg,
        **kw,
    ):
        name = name or f"uid:{random.randint(1, 1000)}"
        self.name = name
        # tasks to be included or excluded
        self.include = include or [".*"]
        self.exclude = exclude or []

        self.progress = Progress(label=self.name)

        if not config_path:
            config_path = "config.yaml"
        config_path = expandpath(config_path)
        self.root = os.path.dirname(config_path)
        self.stats_path = os.path.join(self.root, "stats.yaml")

        if not config_path:
            config_path = "config.yaml"
        config_path = expandpath(config_path)

        try:
            with open(config_path, "rt", encoding="utf-8") as f:
                self.cfg = yaml.load(f, Loader=yaml.Loader)
        except Exception:
            self.cfg = {}

        self.cfg.update(kw)

    def __str__(self):
        return f"<{self.__class__.__name__}>:{self.name}"

    def __repr__(self):
        return str(self)

    async def run(self):
        "agent's initial setup"
        await self._create_resources()
        await self.bootstrap()

    async def bootstrap(self):
        "Add the initial tasks to be executed by crawler"
        log.info(">> [%s] entering bootstrap()", self.name)

        # get iWave storages (if any) to get the starting
        # point of the synchronization

        for func, args, kwargs in self._bootstrap():
            log.info("+ [%s] %s(%s, %s)", self.name, func, args, kwargs)
            target = kwargs.get(KIND_KEY)  #  must exists!
            wave0 = await self._get_initial_wave(target)
            if not wave0:
                log.warning(
                    "Can't find initial sync wave for target URI: [%s]",
                    target,
                )
            else:
                kwargs.setdefault(MONOTONIC_KEY, wave0)

            self.add_task(func, *args, **kwargs)
        log.info("<< [%s] exit bootstrap()", self.name)

    # async def bootstrap(self):
    # "Add the initial tasks to be executed by crawler"

    async def _get_initial_wave(self):
        return 0

    def _bootstrap(self):
        """Provide the initial tasks to ignite the process

        yield a tuple with:
          - function to be executed | name of the function (to be located in any iBot instance)
          - args (call args, if any)
          - kwargs (call kwargs, if any)

        Note: KIND_KEY is the name of the item kind to be synced
              Must match the mapper name in MAPPERS
        """
        return []

    def add_task(self, func, *args, **kw):
        "add a new pending task to be executed by this iAgent"
        raise NotImplementedError()

    async def _create_resources(self):
        "create/start the agent's resources needed before starting"

    async def _stop_resources(self):
        "stop/release the agent's resources on exit"


# ---------------------------------------------------------
# iPlugin
# ---------------------------------------------------------
class iPlugin:
    "A plugin that manipulate received data before giving to main crawler"
    SPECS = {}

    def __init__(self, bot=None, specs=None):
        self.bot = bot
        specs = {} if specs is None else specs
        self.specs = overlap(specs, self.SPECS, overwrite=True)
        self.stats = {}

    def handle(self, data, **context):
        return data, context

    @classmethod
    def matches(self, serie, *patterns):
        for string in serie:
            string = str(string)
            for pattern in patterns:
                if re.match(pattern, string):
                    yield string


class iStreamPlugin(iPlugin):
    """Plugins that received the whole stream instead single data"""


class iPrePlugin(iStreamPlugin):
    """Plugins that must be executed at the beginning of process, just once"""

    SPECS = {
        **iPlugin.SPECS,
    }


class iPostPlugin(iStreamPlugin):
    """Plugins that must be executed at the end of process, just once"""

    SPECS = {
        **iPlugin.SPECS,
    }


class iEachPlugin(iPlugin):
    """Plugins that must be executed for each data received"""

    SPECS = {
        **iPlugin.SPECS,
    }


class NormalizeStreamKeys(iPrePlugin):
    NEED_KEYS = {
        "result": r"result|data",
        "meta": r"meta|info",
    }

    def handle(self, stream, **context):
        #  try to find if match the typical structure

        assert isinstance(stream, list)
        _stream = []
        for item in stream:
            if isinstance(item, dict):
                _item = {}
                used = set()
                for key, pattern in self.NEED_KEYS.items():
                    for k, v in item.items():
                        if re.match(pattern, k):
                            _item[key] = v
                            used.add(k)
                            break
                # complement with not used keys
                for k in used.symmetric_difference(item):
                    _item[k] = item[k]

                # if not set(_item).difference(self.NEED_KEYS):
                # _stream.append(_item)
                _stream.append(_item)
            else:
                _stream.append(item)
        stream = _stream
        return stream, context


class UnwrapStream(iPrePlugin):
    NEED_KEYS = {
        "result",
        "meta",
    }

    def handle(self, stream, **context):
        #  try to find if match the typical structure
        #  TODO: review with josega Multimedia Stats crawler
        assert isinstance(stream, list)
        _stream = []
        for data in stream:
            if isinstance(data, dict) and self.NEED_KEYS.issubset(data):
                _data = data["result"]
                if isinstance(_data, list):
                    _stream.extend(_data)
                    soft(context, data["meta"])
                    continue
            _stream.append(data)
        return _stream, context


# ---------------------------------------------------------
# Bot
# ---------------------------------------------------------
PLUGIN_FAMILIES = set([iPrePlugin, iEachPlugin, iPostPlugin])
"the allowed flow execution families for any plugin"


class iBot(iAgent):
    "Interface for a bot"

    MAX_RETRIES = 15
    DEFAULT_PARAMS = {}
    ALLOWED_PARAMS = [".*"]
    # allowed params from context to build the query

    EXCLUDED_PARAMS = list(parse_uri(""))

    MAX_QUEUE = 200
    DONE_TASKS = {}  # TODO: review faster method

    def __init__(
        self,
        result_queue: Queue,
        *args,
        parent=None,
        context=None,
        headers=None,
        **kw,
    ):
        super().__init__(*args, **kw)
        self.result_queue = result_queue
        self.fiber = None
        self.task_queue = asyncio.queues.Queue()
        self._wip = []
        self.plugins = {}
        self.parent = parent

        context = context or {}
        self.headers = headers or {}
        self.context = {
            **context,
            **self.headers,
            **kw,
        }

        self._sessions: Dict[str, iSession] = {}

    @classmethod
    def clean(cls):
        "clean shared (classmethod) data"
        cls.DONE_TASKS.clear()

    def add_plugin(self, plugin: iPlugin):
        "add a new plugin to be executed by this iBot grouped by some PLUGIN_FAMILIES"
        assert isinstance(
            plugin, iPlugin
        ), f"{plugin} is not a subclass of iPlugin!"
        for klass in PLUGIN_FAMILIES:
            if isinstance(plugin, klass):
                self.plugins.setdefault(klass, []).append(plugin)
                break
        else:
            raise RuntimeError(
                f"plugin: {plugin} does not belongs to {PLUGIN_FAMILIES} allowed classification categories"
            )
        if not plugin.bot:
            plugin.bot = self

    def can_handle(self, func, *args, **kw):
        "return if the function can be handled by this iBot"
        return True

    def process(self, klass, data: Dict | List[Dict], **context):
        "chain execution for all plugins of the given `klass` or transforming the data"
        # check the data received with the kind of pluggin
        if issubclass(klass, iStreamPlugin):
            if not isinstance(data, list):
                raise RuntimeError(
                    f"for plugins [{klass}], data must be a list of dict"
                )
        elif issubclass(klass, iEachPlugin):
            if not isinstance(data, dict):
                raise RuntimeError(
                    f"for plugins [{klass}], data must be a dict"
                )

        for plugin in self.plugins.get(klass, []):
            data, context = plugin.handle(data, **context)
            if not data:
                break
        return data, context

    def add_task(self, func, *args, **kw):
        "add a new pending task to be executed by this iBot"
        universe = list(kw.values()) + list(args)

        def check():
            for string in universe:
                string = str(string)
                for pattern in self.include:
                    if re.match(pattern, string):
                        return True
                for pattern in self.exclude:
                    if re.match(pattern, string):
                        return False

        if check():
            if isinstance(func, str):
                # must be processed by parent
                if self.parent:
                    self.parent.add_task(func, *args, **kw)
                else:
                    log.warning(
                        "[%s] hasn't parent trying to process: %s(%s, %s)",
                        self.name,
                        func,
                        args,
                        kw,
                    )
            else:
                # process itself
                self.task_queue.put_nowait((func, args, kw))

    async def _add_plugins(self):
        # add plugins
        self.add_plugin(Cleaner())

    async def run(self):
        "the entry point / main loop of a single `fiber` in pool"
        progress = Progress(label=self.name)

        log.info(">> [%s] entering run()", self.name)
        await self._add_plugins()
        await super().run()

        last_announce = 0
        while True:
            try:
                while (
                    pending := self.result_queue.qsize()
                ) > self.MAX_QUEUE:
                    now = time.time()
                    if now - last_announce > 10:
                        print(
                            f"Pause worker due too much results pending in queue: {pending}"
                        )
                    last_announce = now
                    await asyncio.sleep(1)

                progress.update(pending=pending)

                # Get a task from the queue
                task = await asyncio.wait_for(
                    self.task_queue.get(), timeout=5
                )
                if task is None:
                    break  # Break the loop
                try:
                    self._wip.append(1)
                    func, args, kwargs = task
                    # print(f">> Processing task: {args}: {kwargs}")
                    if isinstance(func, str):
                        func = getattr(self, func)
                    assert isinstance(func, Callable)
                    kwargs[FUNC_KEY] = func
                    async for data in func(*args, **kwargs):
                        item = task, data
                        await self.result_queue.put(item)
                except Exception as why:
                    log.error(why)
                    log.error(
                        "".join(traceback.format_exception(*sys.exc_info()))
                    )
                finally:
                    self._wip.pop()
                # print(f"<< Processing task: {func}")
            except queue.Empty:
                pass
            except asyncio.exceptions.TimeoutError:
                pass
            except Exception as why:
                log.error(why)
                log.error(
                    "".join(traceback.format_exception(*sys.exc_info()))
                )

        log.info("<< [%s] exit run()", self.name)

    async def dispatch(self, task, data, *args, **kw):
        "do nothing"
        log.info(" - dispatch: %s: %s ; %s, %s", task, data, args, kw)

    def remain_tasks(self):
        "compute how many pending tasks still remains"
        return len(self._wip) + self.task_queue.qsize()

    async def _get_session(self, url, **context) -> iSession:
        uri = parse_uri(url)
        session = self._sessions.get(uri["xhost"])
        if session is None:
            session = self._sessions[uri["xhost"]] = await iSession.new(
                url, bot=self, **context
            )
        return session

    async def get_data(self, **context):
        """
        Example a crawling function for recommender crawler.

        Get data related to the given kind and path.
        May add more tasks to be done by crawler.
        """
        context = {
            CRAWLER_KEY: self.parent,
            BOT_KEY: self,
            # "limit": 50,
            # "offset": 0,
            **context,
        }
        # method to gather the information from 3rd system
        stream, meta = await self._get_data(**context)
        if not stream:
            return

        if isinstance(
            stream,
            (
                list,
                types.GeneratorType,
            ),
        ):
            ##log.debug("received (%s) items of type '%s'", len(stream), context['kind'])
            pass
        else:
            ##log.debug("received a single items of type: '%s'", context['kind'])
            stream = [stream]

        context.update(meta)

        # transform the stream if needed before proccesing each item
        stream, context = self.process(iPrePlugin, stream, **context)

        # process each item from stream
        for _, org in enumerate(stream):
            # data = {**data, **org}

            data = {**org}
            data, ctx = self.process(iEachPlugin, data, **context)

            yield data, (ctx, org)
            # if random.random() < 0.05:
            # await asyncio.sleep(0.25)  # to be nice with other fibers
            ##log.debug("[%s]:[%s]#%s: processed", i, context['kind'], data.get('id', '-'))

        # last chance to execute any action or request more data
        # based on the received stream, i.e. pagination, stats, etc
        stream, context = self.process(iPostPlugin, stream, **context)

    async def _get_data(self, path="", **context):
        "A helper method to get the data from external system"

        soft(context, self.DEFAULT_PARAMS)
        # TODO: MONOTONIC_KEY context must be passed to iSession
        params = self._build_params(**context)

        uri = parse_uri(path)
        if analyze_url(uri)["no_host"]:
            uri2 = self.context["app_url"]  # must exists!
            uri2 = parse_uri(uri2)
            uri["path"] = uri2["path"] = (uri2["path"] or "") + (
                uri["path"] or ""
            )
            uri = overlap(uri2, uri, overwrite=True)

        # since = params.pop(MONOTONIC_SINCE, None)
        # if since:
        # params.update(since)
        uri["query_"] = params

        url = build_uri(**uri)
        if self._is_already(url):
            log.info("[%s] SKIPPING %s : %s", self.name, url, params)
        else:
            self._set_already(url)
            try:
                # get the session related to this url
                proxy = await self._get_session(url, **context)

                # provide extra params to the proxy before calling EP
                call_kw = await proxy.update_params(url, params, context)

                for tries in range(1, self.MAX_RETRIES):
                    try:
                        # authenticate when is needed
                        await proxy.authenticate(url, params)
                        # a chance to create a more specific instance in a context
                        # to deal with the real get() method
                        async with proxy as session:
                            # log.debug(
                            # "[%s][%s/%s] %s : %s", self.name, tries, self.MAX_RETRIES, url, params
                            # )
                            # merge headers without key conflicts
                            soft(call_kw["headers"], self.headers)
                            method = getattr(
                                session, context.get(METHOD_KEY, "get")
                            )
                            response = await method(**call_kw)

                            async with response:
                                if 200 <= response.status < 300:
                                    stream, meta = (
                                        await proxy._process_response(
                                            response
                                        )
                                    )
                                    soft(meta, params)
                                    return stream, meta
                                #  https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#client_error_responses
                                elif response.status in (401, 403, 404, 407):
                                    # forbidden
                                    result = await response.json()
                                    log.error(
                                        "[%s] server sent: %s",
                                        response.status,
                                        result,
                                    )
                                    await proxy.authenticate(url, params)
                                    await asyncio.sleep(0.1)
                                    continue
                                elif 400 <= response.status < 500:
                                    log.warning(
                                        "Status: %s, ABORT, not recoverable error",
                                        response.status,
                                    )
                                    ##log.debug("%s: %s: %s", response.status, path, params)
                                    result = await response.json()
                                    log.error("server sent: %s", result)
                                    raise NonRecoverable(result)
                                elif 500 <= response.status < 600:
                                    log.warning(
                                        "Status: %s, RETRY", response.status
                                    )
                                    ##log.debug("%s: %s: %s", response.status, path, params)
                                    # result = await response.json()
                                    # log.error("server sent: %s", result)
                                else:
                                    log.error("Status: %s", response.status)
                    except NonRecoverable:
                        break
                    except Exception as why:
                        log.error(why)
                        log.error(
                            "".join(
                                traceback.format_exception(*sys.exc_info())
                            )
                        )
                    log.warning("retry: %s: %s, %s", tries, path, params)
                    await asyncio.sleep(0.5)
            finally:
                # self._set_already(url)
                pass
        return None, None

    def _build_params(self, **context):
        params = {}

        def match(text) -> bool:
            if re.match(REG_PRIVATE_KEY, text):
                return False

            if text in self.EXCLUDED_PARAMS:
                return False

            for pattern in self.ALLOWED_PARAMS:
                if re.match(pattern, text):
                    return True

            return False

        # TODO: remove / deprecated
        if "kind" in context:
            log.warning(
                "['%s'] key is deprecated, use KIND_KEY instead", "kind"
            )
            context[KIND_KEY] = context.pop("kind")

        for k, v in context.items():
            if match(k) and isinstance(v, (int, str, float)):
                params[k] = v

        return params

    def _is_already(self, url):
        blueprint = hashlib.md5(url.encode("utf-8")).hexdigest()
        return blueprint in self.DONE_TASKS

    def _set_already(self, url):
        if not self._is_already(url):
            blueprint = hashlib.md5(url.encode("utf-8")).hexdigest()
            self.DONE_TASKS[blueprint] = time.time()
            return True
        return False


# ---------------------------------------------------------
# Helper Plugins
# ---------------------------------------------------------
class Cleaner(iEachPlugin):
    SPECS = {
        **iEachPlugin.SPECS,
    }

    def handle(self, data, **context):
        for k, v in data.items():
            if isinstance(v, str):
                data[k] = v.strip()
        return data, context


class RegExtractor(iEachPlugin):
    # example for gitLab
    SPECS = {
        **iEachPlugin.SPECS,
    }

    def handle(self, data, **context):
        # TODO: review
        # TODO: create a reveal + regexp + SEP ?

        aux = {**data, **context}
        values = list([aux[x] for x in self.matches(aux, "path")])

        # for key in self.matches(aux, KIND_KEY):
        # kind = aux[key]
        for regexp in self.specs:
            for value in values:
                m = re.match(regexp, value)
                if m:
                    data.update(m.groupdict())
        return data, context


class Restructer(iEachPlugin):
    # example for gitLab
    SPECS = {
        **iEachPlugin.SPECS,
    }

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.__mask_restruct_data()

    def __mask_restruct_data(self):
        for container in self.specs.values():
            for k in list(container):
                if SEP in k:
                    continue
                v = container.pop(k)
                k = k.replace("/", SEP)
                v = tuple([v[0].replace("/", SEP), *v[1:]])
                container[k] = v

    def handle(self, data, **context):
        restruct = {}
        kind = context.get(KIND_KEY, UNKNOWN)
        info = self.specs.get("default", {})
        info.update(self.specs.get(kind, {}))
        reveal = build_paths(data)
        for path, value in reveal.items():
            for pattern, (new_path, new_value) in info.items():
                m = re.match(pattern, path)
                if m:
                    d = m.groupdict()
                    d["value"] = value
                    key = tuple(new_path.format_map(d).split(SEP))
                    _value = (
                        value
                        if new_value == COPY
                        else new_value.format_map(d)
                    )
                    restruct[key] = _value

        restruct = rebuild(restruct, result={})
        data = {**data, **restruct}

        return data, context


class FQIUD(iEachPlugin):
    SPECS = {
        **iEachPlugin.SPECS,
        "root": ("{url}", I, "url"),
        # 'groups': ("{id}", int, 'id'),
    }

    def handle(self, data, **context):
        patterns = context.get("kind_key", KIND_KEY)
        for key in self.matches(data, patterns):
            kind = data[key]
            for specs in self.specs.get(kind, []):
                if not specs:
                    continue
                uid_key, func, id_key = specs
                try:
                    uid = uid_key.format_map(data)
                    fquid = func(uid)
                    data[id_key] = fquid
                    data["_fquid"] = fquid
                    data["_uid"] = uid
                    return data
                except Exception as why:
                    # TODO: remove, just debugging
                    log.error(why)
                    log.error(
                        "".join(traceback.format_exception(*sys.exc_info()))
                    )
        return data, context


class Tagger(iEachPlugin):
    SPECS = {
        **iEachPlugin.SPECS,
    }

    def handle(self, data, **context):
        return data, context


class DeepSearch(iEachPlugin):
    SPECS = {
        **iEachPlugin.SPECS,
    }

    def handle(self, data, **context):
        aux = {**data, **context}
        patterns = aux.get("kind_key", KIND_KEY)

        for key in self.matches(aux, patterns):
            kind = aux.get(key)
            for specs in self.specs.get(kind, []):
                if not specs:
                    continue
                try:
                    sub_kind, sub_url = specs
                    sub_url = sub_url.format_map(aux)
                    aux[key] = sub_kind
                    aux["path"] = sub_url

                    self.bot.add_task(
                        func="get_data",
                        **aux,
                    )
                except Exception as why:
                    # TODO: remove, just debugging
                    log.error(why)
                    log.error(
                        "".join(traceback.format_exception(*sys.exc_info()))
                    )

        return data, context


class PaginationDisabled:
    "represent no pagination for an item"


class iPaginationPlugin(iPostPlugin):
    PER_PAGE = "per_page"

    MAX_PAGES = "max_pages"
    FIRST_PAGE = "first_page"
    AHEAD_PAGES = "ahead_pages"
    PAGE = "page"

    FIRST_ITEM = "first_item"
    MAX_ITEMS = "max_items"
    OFFSET = "offset"


class GenericPagination(iPaginationPlugin):

    SPECS = {
        **iPostPlugin.SPECS,
        **{
            DEFAULT: {
                iPaginationPlugin.MAX_ITEMS: "count",
                iPaginationPlugin.MAX_PAGES: "max_pages",
                iPaginationPlugin.OFFSET: "offset",
                iPaginationPlugin.PER_PAGE: "limit",
                iPaginationPlugin.FIRST_ITEM: 0,
            },
            "gitlab": {
                iPaginationPlugin.PAGE: "page",
                iPaginationPlugin.PER_PAGE: "per_page",
                iPaginationPlugin.FIRST_PAGE: 1,
                iPaginationPlugin.AHEAD_PAGES: 1,
            },
        },
    }

    def handle(self, data, **context):
        "Request the next pagination (just the next one!)"

        for name, spec in self.specs.items():
            page = int(context.get(spec[self.PAGE], -1))
            per_page = int(context.get(spec[self.PER_PAGE], 50))
            if context.get(spec.get(self.MAX_ITEMS), -1) < page * per_page:
                page = max(page, spec.get(self.FIRST_PAGE, 0))
                for batch in range(spec.get(self.AHEAD_PAGES, 1)):
                    context[spec[self.PAGE]] = page + 1
                    ##log.debug("> request: %s", context)
                    self.bot.add_task(
                        func="get_data",  # TODO: extract from context
                        # **data,
                        **context,
                    )
                break
        return data, context


class SimplePagination(iPaginationPlugin):
    """
    kind: specs_for_this_kind

    used: kind: [] to explicit avoid pagination
    DEFAULT: a default pagination when no other is defined
    """

    SPECS = {
        # **iPostPlugin.SPECS, # don't use base class
        **{
            DEFAULT: {
                iPaginationPlugin.PAGE: "page",
                iPaginationPlugin.PER_PAGE: "per_page",
                iPaginationPlugin.FIRST_PAGE: 1,
                iPaginationPlugin.AHEAD_PAGES: 1,
            },
            # "groups": {},
            # "projects": {},
            # "users": {},
            # "wikis": {},
            # "issues": {},
            # "milestones": {},
            # "notes": {},
        },
    }

    def handle(self, stream, **context):
        "Request the next pagination"
        kind = context.get(KIND_KEY, UNKNOWN)
        spec = self.specs.get(kind, self.specs.get(DEFAULT))

        # poi and poi-single
        d = re.match(REG_KIND, kind).groupdict()
        if spec == PaginationDisabled or d["sub"] in (SINGLE,):
            # single items doesn't use pagination
            ##log.debug("skip pagination for '%s'", kind)
            # remove parent pagination context
            kind = d["parent"]
            spec = self.specs.get(kind, self.specs.get(DEFAULT))
            if spec:
                foo = 1
            for k in spec.values():
                context.pop(k, None)
            foo = 1
        else:
            ##log.debug("for '%s' use pagination: %s", kind, spec)
            ##log.debug("page: %s, per_page: %s", page, per_page)

            # we have 2 options: pagination based on pages or based on num items
            per_page = int(context.get(spec.get(self.PER_PAGE), 20))
            max_items = context.get(spec.get(self.MAX_ITEMS))
            page = context.get(spec.get(self.PAGE))
            offset = int(context.get(spec.get(self.OFFSET), -1))
            offset = max(offset, spec.get(self.FIRST_ITEM, 0))
            if max_items is not None:
                if max_items > offset:
                    for batch in range(spec.get(self.AHEAD_PAGES, 1)):
                        context[spec[self.OFFSET]] = offset + per_page
                        ##log.debug("> request page: [%s]:%s", kind, context.get(spec[self.PAGE], -1))

                        # use name instead callable so crawler can assign the
                        # request to another bot apartt current one
                        # using calleable will always assign the task to itself
                        func_name = context[FUNC_KEY].__name__

                        self.bot.add_task(
                            func=func_name,
                            # **data,
                            **context,
                        )

            elif page is not None:
                page = max(offset, spec.get(self.FIRST_PAGE, 0))
                max_pages = max(
                    page, spec.get(self.MAX_PAGES, sys.float_info.max)
                )

                if max_pages >= page:
                    for batch in range(spec.get(self.AHEAD_PAGES, 1)):
                        context[spec[self.PAGE]] = page + per_page
                        ##log.debug("> request page: [%s]:%s", kind, context.get(spec[self.PAGE], -1))
                        self.bot.add_task(
                            func="get_data",  # TODO: extract from context
                            # **data,
                            **context,
                        )

            else:
                log.debug("no pagination info found")

        return stream, context


# ---------------------------------------------------------
# HTTP Bots
# ---------------------------------------------------------


class HTTPSession(iSession):

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self._session = None

    def __enter__(self, *args, **kw):
        if self._session is None:
            self._session = aiohttp.ClientSession()
        return self._session

    async def _create_connection(self, url, **kw):
        uri = parse_uri(url, **kw)
        return aiohttp.ClientSession(base_url=uri["xhost"])


iSession.SESSION_FACTORY[r"(http|https)://"] = HTTPSession
# HTTPSession.register(r"(http|https)://")


class TextLinesSession(HTTPSession):
    "An example of session with authentication with an external service"

    async def _process_response(self, response):
        stream, meta = await super()._process_response(response)
        _stream = []
        for data in stream:
            for line in data["result"].splitlines():
                item = {"result": line}
                _stream.append(item)
        return _stream, meta


class HTTPBot(iBot):
    "Basic HTTPBot"

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        self.headers = {
            # USER_AGENT: f"python-{self.__class__.__name__.lower()}/{__version__}",
            USER_AGENT: "Mozilla/5.0 (X11; Linux i686; rv:125.0) Gecko/20100101 Firefox/125.0",
            CONTENT_TYPE: APPLICATION_JSON,
            # "Authorization": f"Bearer {personal_access_token}",
        }

    async def _add_plugins(self):
        await super()._add_plugins()
        self.add_plugin(NormalizeStreamKeys())
        self.add_plugin(UnwrapStream())

        # self.add_plugin(RegExtractor())
        # self.add_plugin(Cleaner())
        # self.add_plugin(FQIUD())
        # self.add_plugin(DeepSearch())
        # self.add_plugin(SimplePagination())


# ---------------------------------------------------------
# SQL Bots
# ---------------------------------------------------------
class iSQLSession(iSession):
    "base class for SQL Based Sessions"
    DEFAULT_METHOD = "post"
    ELAPSED_KEYS = r"(?imux)(duration|elapsed)"
    SENTENCE_KEY = "stmt"

    RESULT_STRUCTURE = {}

    def _get_connection_key(self, _uri: DURI):
        namespace = tf(_uri.get("fscheme", DEFAULT_NAMESPACE))
        # database = tf(uri.get("host", DEFAULT_DATABASE))
        database = _uri["path"]
        key = namespace, database
        return key

    async def get_samples(self, _uri: DURI, N=10):
        # get connection
        conn = await self._get_connection(_uri)

        # get some data
        kind = _uri[KIND_KEY]
        _kind = parse_duri(kind)
        sql = f"SELECT * FROM {_kind['_path']} LIMIT {N}"
        return await self._execute(conn, sql)

    async def _execute(self, connection, sql, **params):
        result = connection.execute(sql, **params)
        return result.fetchall()

    def _map_result_structure(self, data, rows=1, **kw) -> Dict:
        """try to map the info from the structure returned
        from a simple typicl query with the keys that we expect:
        i.e: 'names', 'data', 'elapsed'
        """
        result = {}
        candidates = set(["cols"])
        keys = list(data.keys())
        # iterate in a particular order: candidates + rest from data
        for key in chain(
            candidates.intersection(keys),
            candidates.symmetric_difference(keys),
        ):
            value = data[key]
            if isinstance(value, list):
                if all([_.__class__ == str for _ in value]):
                    result["names"] = key
                elif len(value) == rows:
                    result["data"] = key
            elif isinstance(value, float):
                if re.match(self.ELAPSED_KEYS, key):
                    result["elapsed"] = key
        return result

    async def _inspect_schema(self, _uri: DURI) -> StructShema:
        """Guess table schema by inspecting returned data.
        Session is authenticad already.
        """
        N = 10
        data = await self.get_samples(_uri, N)
        struct = self._map_result_structure(data, rows=N)

        names, types, d_fields, monotonic_since_key = self.guess_schema(
            data[struct['names']], data[struct['data']]
        )
        schema = StructShema(
            names, types, d_fields, monotonic_since_key, struct
        )
        return schema

    async def update_params(self, url: URI, params: JSON, context: JSON):
        "last chance to modify params based on context for a specific iSession type"
        call_kw = await super().update_params(url, params, context)

        _uri = parse_uri(url, **context)
        _uri["query_"].update(params)
        schema = self._schema(_uri) or await self._get_schema(_uri)

        since_key = params.get(MONOTONIC_SINCE_KEY)
        table = context[KIND_KEY]
        if since_key in schema.names:
            query = f"SELECT * FROM {table} WHERE {since_key} > :{MONOTONIC_SINCE_VALUE}"
        else:
            query = f"SELECT * FROM {table}"

        call_kw.setdefault("json", {})[self.SENTENCE_KEY] = query
        return call_kw

    async def _process_response(self, response):
        stream, meta = await super()._process_response(response)

        rows = stream.pop(self.RESULT_STRUCTURE["data"])
        meta["count"] = len(rows)

        for key, value in self.RESULT_STRUCTURE.items():
            if value in stream:
                meta[key] = stream[value]
        cols = meta["names"]

        _stream = []
        for row in rows:
            item = {cols[i]: value for i, value in enumerate(row)}
            _stream.append(item)

        return _stream, meta

    async def get(self, url, headers=None, params=None, **kw):
        headers = headers or {}
        params = params or {}

        _uri = parse_uri(url)
        _uri["query_"].update(params)
        _uri.setdefault(KIND_KEY, self.context[KIND_KEY])

        schema = self._schema(_uri) or await self._get_schema(_uri)

        # # check SINCE
        # since_key = params.get(MONOTONIC_SINCE_KEY)
        # if since_key in fields:
        #     query = f"SELECT * FROM {table} WHERE {since_key} > :{MONOTONIC_SINCE_VALUE}"
        # else:
        #     query = f"SELECT * FROM {table}"

        sql = kw['json']['stmt']
        # connection = sqlite3.connect(_uri["path"])
        # cursor = connection.cursor()
        conn = await self._get_connection(_uri)
        res = await self._execute(conn, sql, **_uri.get("query_", {}))

        data = res[schema.struct['data']]
        body = [
            {schema.names[i]: v for i, v in enumerate(row)} for row in data
        ]

        response = iResponse(
            status=200, headers=headers, links=None, real_url=url, body=body
        )
        return response


class SQLiteSession(iSQLSession):
    "Based on sqlite, change methods as needed"

    DEFAULT_METHOD = "get"

    async def hide_inspect_schema(self, uri, kind):
        """
        info
        ({'date': {'name': 'date',
                   'type': 'TEXT',
                   'notnull': 0,
                   'default': None,
                   'pk': 0,
                   'hidden': 0},
          'value': {'name': 'value',
                    'type': 'REAL',
                    'notnull': 0,
                    'default': None,
                    'pk': 0,
                    'hidden': 0}},
         [{'name': 'date',
           'type': 'TEXT',
           'notnull': 0,
           'default': None,
           'pk': 0,
           'hidden': 0},
          {'name': 'value',
           'type': 'REAL',
           'notnull': 0,
           'default': None,
           'pk': 0,
           'hidden': 0}],
         'date')
        """
        connection = sqlite3.connect(uri["path"])
        cursor = connection.cursor()

        columns = "name", "type", "notnull", "default", "pk", "hidden"
        fields = [
            {columns[i]: value for i, value in enumerate(row[1:])}
            for row in cursor.execute(f"PRAGMA table_xinfo({kind});")
        ]
        d_fields = {_["name"]: _ for _ in fields}

        # try to precalculate the MONOTONIC_SINCE_KEY
        # TODO: move to base class
        def best():
            for value in d_fields:
                for pattern in self.MONOTONIC_CANDIDATES:
                    if re.match(pattern, value):
                        return value

        monotonic_since_key = best()
        info = d_fields, fields, monotonic_since_key
        return info

    async def _create_connection(self, uri: DURI, **_uri):
        connection = sqlite3.connect(uri["path"])
        cursor = connection.cursor()
        return cursor

    async def _execute(self, connection, sql, **params):
        res = connection.execute(sql, params)

        result = {
            "cols": [_[0] for _ in res.description],
            "data": [_ for _ in res],
        }
        return result

        ord_fields = [_[0] for _ in res.description]
        # body = [
        #     {ord_fields[i]["name"]: v for i, v in enumerate(row)}
        #     for row in res
        # ]
        body = [{ord_fields[i]: v for i, v in enumerate(row)} for row in res]

        return body

    async def _process_response(self, response):
        # TODO: remove conflict with base class iSQLSession?
        stream, meta = await iSession._process_response(self, response)
        return stream, meta


iSession.SESSION_FACTORY[r"sqlite://"] = SQLiteSession
# SQLiteSession.register(r"sqlite://")


class PostgreSQLSession(iSQLSession):
    "Based on PostgreSQL, change methods as needed"

    async def get(self, url, headers=None, params=None, **kw):
        uri = parse_uri(url)
        headers = headers or {}
        params = params or {}

        connection = sqlite3.connect(uri["xhost"])
        cursor = connection.cursor()
        res = cursor.execute(f"SELECT * FROM {uri['path']}")
        res = res.fetchall()
        response = iResponse(
            status=200, headers=headers, links=None, real_url=url, body=res
        )
        return response


iSession.SESSION_FACTORY[r"postgresql://"] = PostgreSQLSession
# PostgreSQLSession.register(r"postgresql://")


class SQLBot(iBot):
    "Basic SQLBot"

    # RESPONSE_META = ["headers", "links", "real_url"]
    TABLE_NAME = {
        DEFAULT: "{name}",
    }
    "syncmodel table for a particular database schema"
    WAVE_COLUMN_NAME = {
        DEFAULT: MONOTONIC_KEY,
    }
    "wave column for a particular table"

    #
    MAX_RETRIES = 15
    DEFAULT_PARAMS = {}
    ALLOWED_PARAMS = [".*"]
    # allowed params from context to build the query

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        # self.add_plugin(RegExtractor())
        # self.add_plugin(Cleaner())
        # self.add_plugin(FQIUD())
        # self.add_plugin(DeepSearch())
        # self.add_plugin(SimplePagination())
        # self.headers = {
        # "User-Agent": "python-httpbot/0.1.0",
        # "Content-type": "application/json",
        ## "Authorization": f"Bearer {personal_access_token}",
        # }

    async def get_rows(self, **context):
        """
        Example a crawling function for recommender crawler.

        Get data related to the given kind and path.
        May add more tasks to be done by crawler.
        """
        context = {
            # "limit": 50,
            # "offset": 0,
            **context,
        }
        # method to gather the information from 3rd system
        stream, meta = await self._get_rows(**context)
        if not stream:
            return

        if isinstance(stream, list):
            ##log.debug("received (%s) items of type '%s'", len(stream), context['kind'])
            pass
        else:
            ##log.debug("received a single items of type: '%s'", context['kind'])
            stream = [stream]

        context.update(meta)
        for _, org in enumerate(stream):
            # data = {**data, **org}
            data = {**org}
            data, ctx = self.process(iEachPlugin, data, **context)

            yield data, (ctx, org)
            # if random.random() < 0.05:
            # await asyncio.sleep(0.25)  # to be nice with other fibers
            ##log.debug("[%s]:[%s]#%s: processed", i, context['kind'], data.get('id', '-'))

        # params['offset'] = (page := page + len(result))
        data, context = self.process(iPostPlugin, data, **context)

    def _build_params(self, **context):
        params = {}

        def match(text) -> bool:
            for pattern in self.ALLOWED_PARAMS:
                if re.match(pattern, text):
                    return True
            return False

        for k, v in context.items():
            if match(k) and isinstance(v, (int, str, float)):
                params[k] = v
        return params

    async def _get_rows(self, path, **context):
        "A helper method to get the data from external system"

        soft(context, self.DEFAULT_PARAMS)
        params = self._build_params(**context)

        uri = parse_uri(path)
        if not uri["host"]:
            uri2 = self.context["app_url"]  # must exists!
            uri2 = parse_uri(uri2)
            uri["path"] = uri2["path"] = (uri2["path"] or "") + uri["path"]
            uri = overlap(uri2, uri, overwrite=True)
        uri["query_"] = params

        #
        url = build_uri(**uri)
        # print(url)
        if self._is_already(url):
            ##log.info("[%s] SKIPING %s : %s", self.name, url, params)
            foo = 1
        else:
            self._set_already(url)
            try:
                for tries in range(1, self.MAX_RETRIES):
                    try:
                        session = self._get_session()

                        async with aiohttp.ClientSession() as session:
                            # log.debug(
                            # "[%s][%s/%s] %s : %s", self.name, tries, self.MAX_RETRIES, url, params
                            # )
                            async with session.get(
                                url, headers=self.headers, params=params
                            ) as response:
                                if response.status in (200,):
                                    stream, meta = (
                                        await proxy._process_response(
                                            response
                                        )
                                    )
                                    soft(meta, params)
                                    return stream, meta
                                elif response.status in (400, 404):
                                    log.warning(
                                        "Status: %s, RETRY", response.status
                                    )
                                    ##log.debug("%s: %s: %s", response.status, path, params)
                                    # result = await response.json()
                                    # log.error("server sent: %s", result)
                                elif response.status in (403,):
                                    log.error(
                                        "Status: %s, SKIPPING",
                                        response.status,
                                    )
                                else:
                                    log.error("Status: %s", response.status)
                    except Exception as why:
                        log.error(why)
                        log.error(
                            "".join(
                                traceback.format_exception(*sys.exc_info())
                            )
                        )
                    log.warning("retry: %s: %s, %s", tries, path, params)
                    await asyncio.sleep(0.5)
            finally:
                # self._set_already(url)
                pass
        return None, None

    def _is_already(self, url):
        return url in self.DONE_TASKS

    def _set_already(self, url):
        if not self._is_already(url):
            self.DONE_TASKS[url] = time.time()
            return True
        return False


# ---------------------------------------------------------
# Crawler
# ---------------------------------------------------------
class iCrawler(iAgent):
    "Interface for a crawler"
    bots: Dict[Any, iBot]

    def __init__(
        self, syncmodel: SyncModel, raw_storage=None, prefix="", *args, **kw
    ):
        super().__init__(*args, **kw)
        self.prefix = prefix
        self.bot: Dict[str, iBot] = {}
        self.round_robin: deque[iBot] = deque()
        self.result_queue = Queue()

        self.stats = {}
        self.show_stats = True

        self.syncmodel = list_of(syncmodel, SyncModel)
        self.raw_storage = raw_storage

        self.app_url = self.cfg.get("app_url")
        # self.app_url = (
        # self.cfg["app_url_dev"] if app_url else self.cfg["app_url"]
        # )
        self._app_uri = parse_uri(self.app_url)

    async def run(self) -> bool:
        """TBD"""
        await super().run()

    def _storages(self, klass):
        "get storages that match some class"
        result = []
        for syncmodel in self.syncmodel:
            for storage in syncmodel.storage:
                if isinstance(storage, klass):
                    result.append(storage)

        return result

    def add_task(self, func, *args, **kw):
        "add a new pending task to be executed by a bot that match the profile"
        assert isinstance(
            func, str
        ), f"'func' must be a function name, not {func}"

        # overlap(kw, self._app_uri)
        candidates = self.round_robin
        for _ in range(len(candidates)):
            candidates.rotate(-1)
            bot = candidates[-1]
            if call := getattr(bot, func):
                if bot.can_handle(func, *args, **kw):
                    bot.add_task(call, *args, **kw)
                    break
        else:
            log.warning(
                "can't find a callable for `%s` in (%s) bots",
                len(candidates),
            )

    def remain_tasks(self):
        "compute how many pending tasks still remains"
        n = self.result_queue.qsize()
        for bot in self.bot.values():
            n += bot.remain_tasks()
        return n


class iAsyncCrawler(iCrawler):
    """A crawler that uses asyncio"""

    # need to be redefined by subclass
    MODEL = None
    BOTS = [HTTPBot]

    # governance data
    MAPPERS = {}
    RESTRUCT_DATA = {}
    RETAG_DATA = {}
    REFERENCE_MATCHES = []
    KINDS_UID = {}

    def __init__(self, fibers=3, *args, **kw):
        super().__init__(*args, **kw)
        self.fibers = fibers
        self.t0 = 0
        self.t1 = 0
        self.nice = 600
        self.model = self.MODEL() if self.MODEL else None

    async def _get_initial_wave_old(self, kind):
        # TODO: use URI
        waves = []
        storage = None
        for storage in self._storages(klass=WaveStorage):
            # last_waves(self, sources: List, uid: UID) -> Dict[str, WAVE]:
            klass = self.MAPPERS.get(kind)
            if klass:
                waves.extend(await storage.last_wave(klass.PYDANTIC))
            else:
                log.error("[%s] kind hasn't a MAPPER class defined", kind)

        if not storage:
            log.error(
                "[%s] doesn't use any WaveStorage, it's needed for getting initial wave!",
                self,
            )

        waves.sort(key=lambda x: x.get(MONOTONIC_KEY, 0))
        return waves and waves[0]

    async def _get_initial_wave(self, uri):
        # TODO: use URI
        waves = []
        storage = None
        for storage in self._storages(klass=WaveStorage):
            # last_waves(self, sources: List, uid: UID) -> Dict[str, WAVE]:
            klass = self.MAPPERS.get(uri)
            if klass:
                waves.extend(await storage.last_wave(uri))
            else:
                log.error("[%s] uri hasn't a MAPPER class defined", uri)

        if not storage:
            log.error(
                "[%s] doesn't use any WaveStorage, it's needed for getting initial wave!",
                self,
            )
            raise RuntimeError(
                f"You need to use a WaveStorage in any SyncModel to use waves"
            )

        waves.sort(key=lambda x: x.get(MONOTONIC_KEY, 0))
        return waves and waves[0]

    async def run(self) -> bool:
        """Execute a full crawling loop"""
        await super().run()

        # Create a worker pool with a specified number of 'fibers'
        self.t0 = time.time()
        self.t1 = self.t0 + self.nice

        # wait until all work is done
        while remain := self.remain_tasks():
            try:
                # result = await asyncio.wait_for(self.result_queue.get(), timeout=2)
                # result = await self.result_queue.get()
                result = await asyncio.wait_for(
                    self.result_queue.get(), timeout=2
                )
                res = await self.dispatch(*result)
                if not res:
                    # log.warning(
                    # "Can't save item in storage: %s", result[0][2]
                    # )
                    # log.warning("%s", pformat(result[1]))
                    self.stats["failed"] = self.stats.get("failed", 0) + 1
                    self.progress.closer()
            except queue.Empty:
                pass
            except asyncio.exceptions.TimeoutError:
                pass
            except Exception as why:
                log.error(why)
                log.error(
                    "".join(traceback.format_exception(*sys.exc_info()))
                )

            self.progress.update(
                remain=remain,
                stats=self.stats,
                force=False,
            )

        await self._stop_resources()

        # result = all([await sync.save(wait=True) for sync in self.syncmodel])
        result = await self.save()
        if result:
            log.info("all storages have been saved")
        else:
            log.error("some storages have NOT been SAVED")

        return result

    async def dispatch(self, task, data, *args, **kw):
        "create an item from data and try to update into storage"
        func, _args, _kw = task
        # _kw: {'kind': 'groups', 'path': '/groups?statistics=true'}
        # data:  {'id': 104, ... }
        kind = _kw[KIND_KEY]
        # uid = self.get_uid(kind, data)

        # processed data, (execution context, original data)
        data, (context, org) = data

        # inject item into models
        item = self.new(kind, data)
        if item is None:
            result = False
        else:
            # result = await self.syncmodel.put(item)
            result = all([await sync.put(item) for sync in self.syncmodel])

            # save original item if a raw storage has been specified
            if self.raw_storage:
                fqid = item.id
                await self.raw_storage.put(fqid, org)

            # check if we need to do something from time to time
            t1 = time.time()
            if t1 > self.t1:
                self.t1 = t1 + self.nice
                await self.save(nice=True)

        return result

    async def save(self, nice=False, wait=False):
        log.info("Saving models")
        result = all(
            [
                await sync.save(nice=nice, wait=wait)
                for sync in self.syncmodel
            ]
        )
        if self.raw_storage:
            res = await self.raw_storage.save(nice=nice, wait=wait)
            result = result and res
        return result

    async def _create_resources(self):
        BOTS = deque(self.BOTS)

        for n in range(self.fibers):
            BOTS.rotate()
            klass = BOTS[-1]
            name = f"{klass.__name__.lower()}-{n}"

            klass.clean()

            bot = klass(
                result_queue=self.result_queue,
                name=name,
                parent=self,
                context=self.__dict__,
            )
            self.add_bot(bot)

    def add_bot(self, bot: iBot):
        self.bot[bot.name] = bot
        self.round_robin.append(bot)
        loop = asyncio.get_running_loop()
        bot.fiber = loop.create_task(bot.run())

    async def _stop_resources(self):
        # Add sentinel values to signal worker threads to exit
        for nane, bot in self.bot.items():
            bot.task_queue.put_nowait(None)

    def remain_tasks(self):
        "compute how many pending tasks still remains"
        n = sum([sync.running() for sync in self.syncmodel])
        if self.raw_storage:
            n += self.raw_storage.running()
        n += super().remain_tasks()
        # x = 1
        # n += x
        return n

    def _clean(self, kind, data):
        for k, v in data.items():
            if isinstance(v, str):
                data[k] = v.strip()
        return data

    # Transformer

    def convert_into_references(self, data):
        """Search for nested objects in `value` and convert them into references"""
        if self.REFERENCE_MATCHES:
            id_keys = list(
                walk(
                    data,
                    keys_included=self.REFERENCE_MATCHES,
                    include_struct=False,
                )
            )
            for idkey, idval in id_keys:
                # myassign(value, myget(value, idkey), idkey[:-1])
                myassign(data, idval, idkey[:-1])

        return data

    def new(self, kind, data):
        """Try to create / update an item of `type_` class from raw data

        - convert nested data into references
        - convert data to suit pydantic schema
        - get the pydantic item

        """
        data2 = self.convert_into_references(data)
        d = re.match(REG_KIND, kind).groupdict()
        real_kind = d["parent"]
        klass = self.MAPPERS.get(real_kind)
        if not klass:
            log.warning(
                "missing MAPPERS[%s] class!", kind
            )  # TODO: remove debug
            return

        # check if fquid is well formed
        _id = data2.get("id", kind)
        if not REG_SPLIT_PATH.match(str(_id)):
            if _id is None:
                fquid = f"{kind}"
            else:
                fquid = f"{kind}:{_id}"

            data2["id"] = fquid
        else:
            foo = 1  # data comes with a fquid

        item = klass.pydantic(data2)
        return item

    def _restruct(self, kind, data, reveal):
        """Restructure internal data according to `RESTRUCT_DATA` structure info.

        Finally the result is the overlay of the original `data` and the restructured one.
        """
        restruct = {}
        info = self.RESTRUCT_DATA.get("default", {})
        info.update(self.RESTRUCT_DATA.get(kind, {}))
        for path, value in reveal.items():
            for pattern, (new_path, new_value) in info.items():
                m = re.match(pattern, path)
                if m:
                    d = m.groupdict()
                    d["value"] = value
                    key = tuple(new_path.format_map(d).split(SEP))
                    _value = (
                        value
                        if new_value == COPY
                        else new_value.format_map(d)
                    )
                    restruct[key] = _value

        # build the restructured data
        restruct = rebuild(restruct, result={})
        # create the overlay of both data to be used (possibly) by pydantic
        data = {**data, **restruct}

        return data

    def _transform(self, kind, data):
        return data
