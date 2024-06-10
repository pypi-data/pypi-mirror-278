# ----------------------------------------------------------
# Storage Port
# ----------------------------------------------------------
import asyncio
import os
import pickle
import re
import time
import sys
import traceback
from typing import Dict, List
from multiprocessing import Process
import random
import yaml
from logging import ERROR, INFO, getLogger
import hashlib
import uuid

# from surrealdb import Surreal
from surrealist import Surreal as Surrealist


from agptools.logs import logger
from agptools.helpers import parse_uri, build_uri
from agptools.containers import merge as merge_dict

from .crud import (
    DEFAULT_DATABASE,
    DEFAULT_NAMESPACE,
    parse_duri,
    tf,
    esc,
    iStorage,
    iPolicy,
    iConnection,
)
from .wave import (
    iWaves,
    TUBE_DB,
    TUBE_META,
    TUBE_NS,
    TUBE_SYNC,
    TUBE_WAVE,
)

from syncmodels.http import (
    guess_content_type,
    ALL_JSON,
    CONTENT_TYPE,
    USER_AGENT,
    APPLICATION_JSON,
)
from .requests import iResponse

# from surrealist.connections.connection import logger as surreal_logger
from .exceptions import BadData
from .definitions import (
    FORCE_SAVE,
    MONOTONIC_KEY,
    ORG_KEY,
    UID,
    URI,
    JSON,
    WAVE,
    QUERY,
    filter_4_compare,
    build_fqid,
    REG_SPLIT_PATH,
)
from .helpers import expandpath


# ---------------------------------------------------------
# Loggers
# ---------------------------------------------------------


# from 0.5.2 surreslist uses root default level
for _ in (
    "surrealist.connection",
    "surrealist.connections.websocket",
    "websocket_connection",
):
    getLogger(_).setLevel(ERROR + 1)


log = logger(__name__)


# REGEXP_FQUI = re.compile(r"((?P<ns>[^/]*?)/)?(?P<table>[^:]+):(?P<uid>.*)$")
def split_fqui(fqid):
    try:
        table, uid = fqid.split(":")
        return table, uid
    except ValueError:
        return fqid, None


# ---------------------------------------------------------
# Data Store / Ignore Policies
# ---------------------------------------------------------


class DataInsertionPolicy(iPolicy):
    "when a record must be inserted or not"

    async def action(self, mode, thing, data):
        if mode in (iWaves.MODE_SNAPSHOT,):
            return self.STORE

        if mode in (iWaves.MODE_TUBE,):
            # check if last data is the same but MONOTONIC_KEY
            tube_name = thing.split(":")[0]
            fquid = f"{TUBE_WAVE}:{tube_name}"

            # TODO: use sync or cache for faster execution
            last = await self.storage.last_wave(fquid)
            _last = filter_4_compare(last)
            _data = filter_4_compare(data)
            if _last == _data:
                return self.DISCARD

            return self.STORE

        return self.DISCARD


# ---------------------------------------------------------
# Main Storage interafce proposal
# ---------------------------------------------------------


class Storage(iStorage):
    def __init__(self, url, policy=DataInsertionPolicy):
        super().__init__(url=url, policy=policy)
        self.background = []

    def running(self):
        self.background = [p for p in self.background if p.is_alive()]
        return len(self.background)

    async def info(self):
        raise NotImplementedError()


# ---------------------------------------------------------
# Main Storage interafce proposal
# ---------------------------------------------------------


# ---------------------------------------------------------
# Storages Ports used by hexagonal architecture
# TODO: review if storage may replace them all
# ---------------------------------------------------------


class StoragePort(Storage):
    PATH_TEMPLATE = "{self.url}/{table}"

    def __init__(self, url="./db"):
        super().__init__(url=url)
        url = expandpath(url)
        if not os.path.exists(url):
            os.makedirs(url, exist_ok=True)
        self.url = url
        self.cache = {}
        self._dirty = {}

    def _file(self, table):
        return self.PATH_TEMPLATE.format_map(locals())

    def load(self, table, force=False):
        universe = self.cache.get(table)
        if force or universe is None:
            path = self._file(table)
            if os.path.exists(path):
                try:
                    universe = self._real_load(path)
                except Exception as why:
                    log.warning(why)
            if universe is None:
                universe = {}
            self.cache[table] = universe
        return universe

    _load = load

    def _save(self, table, universe=None, pause=0, force=False):
        if self._dirty.pop(table, force):
            if universe is None:
                universe = self.load(table)
            path = self._file(table)
            self._real_save(path, universe, pause=pause)

    def _real_load(self, path):
        raise NotImplementedError()

    def _real_save(self, path, universe, pause=0):
        raise NotImplementedError()

    async def get(self, fqid, query=None, **params):
        table, uid = split_fqui(fqid)
        universe = self.load(table)
        if query:
            raise NotImplementedError

        data = universe.get(fqid, {})
        return data

    async def set(self, fqid, data, merge=False):
        table, uid = split_fqui(fqid)
        universe = self.load(table)
        if merge:
            data0 = await self.get(fqid)
            # data = {** data0, ** data} # TODO: is faster?
            data0.update(data)
            data = data0

        universe[fqid] = data
        self._dirty[table] = True
        return True

    async def save(self, table=None, nice=False, wait=False):
        table = table or list(self.cache)
        if not isinstance(table, list):
            table = [table]
        for i, tab in enumerate(table):
            pause = 1.0 * i if nice else 0
            self._save(tab, pause=pause)

        log.info("waiting data to be saved")
        while wait and self.running() > 0:
            await asyncio.sleep(0.1)
        return self.running() == 0

    async def info(self, ns=""):
        "Returns storage info: *tables*, etc"
        if ns:
            table = f"{ns}/.*"
        else:
            table = f".*"

        pattern = self._file(table=table)
        top = os.path.dirname(pattern)
        for root, _, files in os.walk(top):
            for file in files:
                path = os.path.join(root, file)
                m = re.match(pattern, path)
                if m:
                    relpath = os.path.relpath(path, self.url)
                    name = os.path.splitext(relpath)[0]
                    yield name


class PickleStorage(StoragePort):
    PATH_TEMPLATE = "{self.url}/{table}.pickle"

    def _real_load(self, path):
        try:
            universe = pickle.load(open(path, "rb"))
        except Exception as why:
            log.error("%s: Error loading: %s: %s", self, path, why)
            universe = {}
        return universe

    def _real_save(self, path, universe, pause=0):
        try:
            log.debug("[%s] saving: %s", self.__class__.__name__, path)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            pickle.dump(universe, open(path, "wb"))
        except Exception as why:
            log.error("%s: Error savig: %s: %s", self, path, why)


def ulid():
    return time.time_ns()


class iMemConnection(iConnection):
    "Memory cache iConnection implementation"

    HEADERS = {
        CONTENT_TYPE: APPLICATION_JSON,
    }

    def __init__(
        self,
        storage: StoragePort,
        namespace=DEFAULT_NAMESPACE,
        database=DEFAULT_DATABASE,
    ):
        super().__init__()
        self.st = storage
        self.ns = namespace
        self.db = database

    def create(self, thing, data, record_id=None):
        """Hack to store items into StoragePorts that uses cache"""

        if record_id is None:
            record_id = data.get('id') or ulid()

        data['id'] = record_id  # to mimicking surreal behaviour

        uri = f'{self.ns}://{self.db}/{thing}:{record_id}'
        # _uri = parse_duri(uri)
        table = self.ns
        self.st.load(table)

        holder = (
            self.st.cache.setdefault(self.ns, {})
            .setdefault(self.db, {})
            .setdefault(thing, {})
        )
        holder[record_id] = data
        self.st._dirty[self.ns] = True

        response = iResponse(
            status=200,
            headers={**self.HEADERS},
            links=None,
            real_url=uri,
            body=data,
            result=data,
        )

        return response

    def update(self, thing, data, record_id=None):
        """Hack to store items into StoragePorts that uses cache"""
        return self.create(thing, data, record_id)

    def query(self, thing, data, record_id=None):
        raise NotImplementedError()

    def select(self, thing, data, record_id=None):
        raise NotImplementedError()

    def use(self, namespace, database):
        self.ns = namespace
        self.db = database


class YamlStorage(StoragePort):
    PATH_TEMPLATE = "{self.url}/{table}.yaml"

    def __init__(self, url="./db"):
        super().__init__(url=url)
        self.lock = 0

    def _real_load(self, path):
        try:
            universe = yaml.load(
                open(path, encoding="utf-8"), Loader=yaml.Loader
            )
        except Exception as why:
            log.error("%s: Error loading: %s: %s", self, path, why)
            universe = {}
        return universe

    def _real_save(self, path, universe, pause=0):
        def main(path, universe, pause):
            # name = os.path.basename(path)
            # log.debug(">> ... saving [%s] in %s secs ...", name, pause)
            time.sleep(pause)
            try:
                log.debug("[%s] saving: %s", self.__class__.__name__, path)
                os.makedirs(os.path.dirname(path), exist_ok=True)
                yaml.dump(
                    universe,
                    open(path, "w", encoding="utf-8"),
                    Dumper=yaml.Dumper,
                )
            except Exception as why:
                log.error("%s: Error savig: %s: %s", self, path, why)
            # log.debug("<< ... saving [%s] in %s secs DONE", name, pause)

        if pause > 0:
            # uses a background thread to save in YAML format
            # because is too slow to block the main thread
            # th = threading.Thread(target=main)
            # th.start()
            p = Process(
                target=main, args=(path, universe, pause), daemon=True
            )
            self.background.append(p)
            p.start()
            # log.debug("saving daemon is running:  %s", p.is_alive())
            foo = 1
        else:
            main(path, universe, pause=0)

    async def _connect(self, *key) -> iConnection:
        url = parse_uri(self.url)
        # url["fscheme"] = "http"
        # url["path"] = ""
        url = build_uri(**url)

        connection = iMemConnection(storage=self)

        self.connections[key] = connection
        namespace, database = key
        connection.use(namespace, database)
        # setattr(connection, "database", database)
        # create initial database layout
        # await self._update_database_layout(connection)
        self._last_connection = connection
        return connection


class DualStorage(PickleStorage):
    """Storage for debugging and see all data in yaml
    Low performance, but is just for testing
    """

    def __init__(self, url="./db", klass=YamlStorage):
        super().__init__(url=url)
        self.other = klass(url)
        self.background = self.other.background

    async def get(self, fqid, query=None, **params):
        other_mtime = None
        if not self.other.lock:
            table, uid = split_fqui(fqid)
            other_path = self.other._file(table)
            mine_path = self._file(table)
            if os.access(other_path, os.F_OK):
                other_mtime = os.stat(other_path).st_mtime
            else:
                other_mtime = 0
            if os.access(mine_path, os.F_OK):
                mine_mtime = os.stat(mine_path).st_mtime
            else:
                mine_mtime = 0

        if other_mtime is not None:
            if other_mtime > mine_mtime:
                # replace table from newer to older one
                universe = self.other._load(table)
                super()._save(table, universe, force=True)
                self.cache[table] = universe
            data = await super().get(fqid, query=None, **params)
        else:
            data = {}
        return data

    def _load(self, table):
        other_mtime = None
        if not self.other.lock:
            other_path = self.other._file(table)
            mine_path = self._file(table)
            if os.access(other_path, os.F_OK):
                other_mtime = os.stat(other_path).st_mtime
            else:
                other_mtime = 0
            if os.access(mine_path, os.F_OK):
                mine_mtime = os.stat(mine_path).st_mtime
            else:
                mine_mtime = 0

        if other_mtime is not None:
            if other_mtime > mine_mtime:
                # replace table from newer to older one
                universe = self.other._load(table)
                super()._save(table, universe, force=True)
                self.cache[table] = universe
            data = super()._load(table)
        else:
            data = {}
        return data

    load = _load

    async def set(self, fqid, data, merge=False):
        """
        other.mtime < mine.mtime
        otherwise user has modifier `yaml` file and `pickle` will be updated
        """
        res1 = await self.other.set(fqid, data, merge)
        res2 = await super().set(fqid, data, merge)
        return all([res1, res2])

    async def put(self, uri: URI, data: JSON = None, **kw) -> bool:
        if data is None:
            data = kw
        else:
            data.update(kw)
        res1 = await super().put(fqid, data)
        res2 = await self.other.put(fqid, data)
        return all([res1, res2])

    def _save(self, table, universe=None, pause=0):
        self.other._save(table, universe, pause=pause)
        super()._save(table, universe, pause=pause)

    def running(self):
        return super().running() + self.other.running()


# ---------------------------------------------------------
# iWave interfaces
# TODO: move to base class or define a new interface
# ---------------------------------------------------------


# TODO: unify with wave.get_tube_name() and move to share place
def get_tube_name(klass):
    if isinstance(klass, str):
        tube_name = klass.split(":")[-1]
    else:
        tube_name = f"{klass.__module__.replace('.', '_')}_{klass.__name__}"
    return tube_name


class WaveStorage(iWaves, iStorage):
    "A mixing of iWave and Storage, using itself as Storage"

    def __init__(
        self,
        url="./db",
        storage: iStorage = None,
        mode=iWaves.MODE_TUBE,
        policy=DataInsertionPolicy,
    ):
        super().__init__(url=url, storage=storage, policy=policy)
        self.mode = mode

    async def put(self, uri: URI, data: JSON = None, **kw) -> bool:
        if data is None:
            data = kw
        else:
            data.update(kw)

        data = data.copy()  # don't alter the caller item
        try:
            if self._has_change(uri, **data):
                _uri = parse_duri(uri)
                # just for clarity
                namespace = _uri["fscheme"]
                database = _uri["host"]
                tube_name = _uri["_path"]
                uid = data.get("id", None)

                # save the last snapshot of the data as last_wave
                # mimicking a context-broker alike storage (Orion:mongo, etc)
                query = f"{namespace}://{database}/{TUBE_WAVE}"
                data["id"] = tube_name
                res1 = await self.storage.put(query, data)
                data.pop("id", None)  #  drop data again

                # transform data and save into storage as `tube` mode
                monotonic = data.pop(MONOTONIC_KEY, time.time_ns())
                data[ORG_KEY] = _uri.get("id") or uid  #  must exists!
                _uri["path"] = f"/{tube_name}:{monotonic}"
                res2 = await self.storage.put(build_uri(**_uri), data)

            return all([res1, res2])
        except Exception as why:
            log.error(why)
            log.error("".join(traceback.format_exception(*sys.exc_info())))

    def running(self):
        return self.storage.running()


# ---------------------------------------------------------
# Surreal Storage
# TODO: move to base class or define a new interface
# ---------------------------------------------------------


# TODO: move this definitions and DB_LAYOUT to a common place

QUERY_UPDATE_TUBE_SYNC = "UPDATE $record_id SET wave__ = $wave__;"
QUERY_SELECT_TUBE_SYNC = (
    f"SELECT * FROM {TUBE_SYNC} WHERE source=$source AND target=$target" ""
)


class SurrealistStorage(Storage):
    MAX_HARD_CONNECTIONS = 250
    DROP_CONNECTIONS = 100
    MAX_RECONNECTION = 10

    DB_INFO = """
    INFO FOR DB;
    """
    DB_LAYOUT = {
        TUBE_META: f"""
        DEFINE TABLE IF NOT EXISTS {TUBE_META} SCHEMALESS;
        -- TODO: set an index properly
        -- TODO: the next sentence will cause an error creating records
        -- DEFINE FIELD id ON TABLE {TUBE_META};
        """,
        # TUBE_WAVE: f"""
        # DEFINE TABLE IF NOT EXISTS {TUBE_WAVE} SCHEMAFULL;
        # DEFINE FIELD id ON TABLE {TUBE_WAVE} TYPE string;
        # DEFINE FIELD wave ON TABLE {TUBE_WAVE} TYPE int;
        # """,
        TUBE_SYNC: f"""
        DEFINE TABLE IF NOT EXISTS {TUBE_SYNC} SCHEMAFULL;
        DEFINE FIELD source ON TABLE {TUBE_SYNC} TYPE string;
        DEFINE FIELD target ON TABLE {TUBE_SYNC} TYPE string;
        DEFINE FIELD {MONOTONIC_KEY} ON TABLE {TUBE_SYNC} TYPE int;
        """,
        f"{TUBE_SYNC}Index": f"""
        DEFINE INDEX IF NOT EXISTS {TUBE_SYNC}Index ON {TUBE_SYNC} COLUMNS source, target UNIQUE;
        """,
    }

    def __init__(
        self,
        url="./db",
        user="root",
        password="root",
        ns="test",
        db="test",
        policy=DataInsertionPolicy,
    ):
        super().__init__(url=url, policy=policy)
        self.cache = {}
        self.user = user
        self.password = password
        self.ns = ns
        self.db = db
        self.surreal = None

    def close(self):
        for key in list(self.connections):
            self._close(key)

    def __del__(self):
        self.close()

    async def start(self):
        "any action related to start storage operations"
        await super().start()
        # _ = self.connection or await self._connect()

    async def stop(self):
        "any action related to stop storage operations"
        await super().stop()
        self.close()

    def _close(self, key):
        conn = self.connections.pop(key)
        # print(f"dropping: {key}")
        try:
            if conn.is_connected():
                conn.close()
        except (
            Exception
        ):  # surrealist.errors.OperationOnClosedConnectionError
            foo = 1

    async def _connect(self, *key):
        connection = self.connections.get(key)
        if connection:
            namespace, database = key
            if getattr(connection, "database", None) != database:
                result = connection.use(namespace, database)
                setattr(connection, "database", database)

            return connection

        url = parse_uri(self.url)
        url["fscheme"] = "http"
        url["path"] = ""
        url = build_uri(**url)

        t0 = time.time()
        if self.surreal is None:
            self.surreal = Surrealist(
                url,
                # namespace=namespace,
                # database=self.db,
                credentials=(self.user, self.password),
                use_http=False,
                timeout=20,
            )
            print(url)

        for i in range(self.MAX_RECONNECTION):
            try:
                # print(self.surreal.is_ready())
                # print(self.surreal.version())
                # print(self.surreal.health())

                connection = self.surreal.connect()

                if len(self.connections) >= self.MAX_HARD_CONNECTIONS:
                    keys = list(self.connections)
                    drops = set()
                    N = len(keys) - 1
                    while len(drops) < self.DROP_CONNECTIONS:
                        drops.add(keys[random.randint(0, N)])

                    for key in drops:
                        self._close(key)
                break
            except Exception as why:
                print(f"[{i}] {why}")
                time.sleep(1)

        # print(f"creating: {key}: elapsed: {elapsed}")
        self.connections[key] = connection
        namespace, database = key
        result = connection.use(namespace, database)
        # setattr(connection, "database", database)
        # create initial database layout
        # await self._update_database_layout(connection)
        self._last_connection = connection
        return connection

        # TODO: use credentials
        # await self.connection.connect()
        # await self.connection.signin({"user": self.user, "pass": self.password})
        # await self.connection.use(self.ns, self.db)

    async def query(self, query: URI | QUERY) -> List[JSON]:
        "Make a query to the system based on URI (pattern)"
        query = parse_duri(query)

        key = (query["fscheme"], query["host"])
        connection = self.connections.get(key) or await self._connect(*key)
        assert connection, "surreal connection has failed"

        _path = query["_path"]  # must exists
        table = tf(_path)

        if params := query.get("query_", {}):
            where = " AND ".join(f"{k}=${k}" for k in params)
            sql = f"SELECT * FROM {table} WHERE {where}"
        else:
            sql = f"SELECT * FROM {table}"

        res = connection.query(sql, variables=params)
        self._last_connection = connection
        return res.result

    async def save(self, nice=False, wait=False):
        "TBD"
        return True  # Nothig to do

    async def since(self, fqid, wave, max_results=100):

        _fqid = tf(fqid)
        query = f"""
        SELECT *
        FROM {_fqid}
        WHERE  {MONOTONIC_KEY} > {wave}
        ORDER BY _wave ASC
        LIMIT {max_results}
        """
        key = TUBE_NS, TUBE_DB
        connection = self.connections.get(key) or await self._connect(key)
        res = connection.query(query)
        return res.result

    async def hide_get(self, fqid, cache=True, mode=None) -> Dict:
        mode = mode or self.mode
        if mode in (self.MODE_SNAPSHOT,):
            if cache:
                data = self.cache.get(fqid)
            else:
                data = None
            if data is None:
                self.connection or await self._connect()
                try:
                    res = self.connection.select(fqid)
                    result = res.result
                    if result:
                        data = result[0]
                except Exception as why:
                    log.warning(why)

                if not cache:
                    self.cache[fqid] = data
            return data
        else:
            raise RuntimeError(f"UNKOWN mode: {mode} for get()")

    async def _update_database_layout(self, connection):
        """
        Check / Create the expected database layout
        """
        # info = self.connection.query(self.DB_INFO)
        # tables = info.result["tables"]
        for table, schema in self.DB_LAYOUT.items():
            # TODO: check tables and individual indexes
            if True or table not in tables:
                # TODO: delete # schema = "USE NS test DB test;" + schema
                result = connection.query(schema)
                if result.status in ("OK",):
                    log.info("[%s] : %s", schema, result.status)
                else:
                    log.error("[%s] : %s", schema, result.status)

    async def hide_put(self, uri: URI, data: JSON = None, **kw) -> bool:
        if data is None:
            data = kw
        else:
            data.update(kw)

        try:
            connection, thing, _uri = await self._prepare_call(uri)
            record_id = _uri["id"] or data.get("id", None)  # must exists!
            record_id = esc(record_id)
            if record_id:
                data.pop(
                    "id", None
                )  # can't use record_id and data['id]. It'll fail in silence
                result = connection.update(thing, data, record_id=record_id)
            else:
                result = connection.create(thing, data)

            return result.result and result.status in ("OK",)  # True|False

        except Exception as why:
            log.error(why)
            log.error("".join(traceback.format_exception(*sys.exc_info())))

    async def update_meta(self, tube, meta, merge=True):
        """Update the tube metadata.
        If merge is Frue, meta-data will me merge
        If merge is False, meta-data will be replace
        """
        fqid = f"{TUBE_META}:{tube}"
        meta["id"] = fqid
        res = self.connection.select(fqid)
        result = res.result
        if result:
            if merge:
                assert len(result) == 1
                _meta = result[0]
                if isinstance(_meta, dict):
                    if all([_meta.get(key) == meta[key] for key in meta]):
                        # don't update anything
                        # so it will not activate any live_query
                        return True
                    meta = merge_dict(_meta, meta)

            result = self.connection.update(
                TUBE_META,
                meta,
            )
        else:
            res = self.connection.create(
                TUBE_META,
                meta,
            )
        return res.status in ("Ok",)

    async def find_meta(self, meta):
        """Find tubes that match the specified meta"""
        if not meta:
            raise RuntimeError(f"meta can't be empty")
        params = " AND ".join([f"{key}=${key}" for key in meta])
        query = f"SELECT * FROM {TUBE_META} WHERE {params}"
        res = self.connection.query(
            query,
            meta,
        )
        if res.status in ("OK",):
            return res.result
        raise RuntimeError(f"bad query: {query}")

    async def info(self, uri=""):
        "TBD"
        if not (conn := self._last_connection):
            _uri = parse_duri(uri)
            key = _uri["fscheme"], _uri["host"]
            conn = self.connections.get(key) or await self._connect(*key)

        result = {}
        for func in ["ns", "db"]:
            result.update(getattr(conn, f"{func}_info")().result)

        return result

    async def count(self, table):
        if not (conn := self._last_connection):
            _uri = parse_duri("")
            key = _uri["fscheme"], _uri["host"]
            conn = self.connections.get(key) or await self._connect(*key)

        result = conn.count(table)
        return result.result
