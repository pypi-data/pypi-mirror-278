import traceback
from typing import List
import random
import re
import sys
import traceback

from agptools.logs import logger
from agptools.helpers import build_uri, parse_xuri
from agptools.containers import overlap


from .definitions import URI, JSON, QUERY, REG_SPLIT_PATH
from .http import STATUS_OK

log = logger(__name__)

# ---------------------------------------------------------
# Default URI handling
# ---------------------------------------------------------

DEFAULT_NAMESPACE = "test"
DEFAULT_DATABASE = "test"
DEFAULT_URI_PARAMS = {
    "fscheme": DEFAULT_DATABASE,
    "host": DEFAULT_DATABASE,
    "xhost": DEFAULT_DATABASE,
}


MAX_HARD_URIS = 200
MAX_SOFT_URIS = 150
last_uris = {}


# ---------------------------------------------------------
# transformation helpers
# ---------------------------------------------------------
def tf(name):
    return re.sub(r"\W", "_", name)


def esc(uid):
    if isinstance(uid, str):
        try:
            uid = int(uid)
        except:
            pass
    return uid


def parse_duri(uri: URI | QUERY, _ignore_cache_=False, **kw) -> QUERY:
    global last_uris
    if isinstance(uri, URI.__supertype__):  # URI
        if _ignore_cache_ or not (_uri := last_uris.get(uri)):
            _uri = parse_xuri(uri)
            if len(last_uris) > MAX_HARD_URIS:
                keys = list(last_uris)
                while n := len(keys) > MAX_SOFT_URIS:
                    last_uris.pop(keys.pop(random.randint(0, n - 1)))
            overlap(_uri, DEFAULT_URI_PARAMS)
            last_uris[uri] = _uri
    elif isinstance(uri, QUERY.__supertype__):
        _uri = uri
        overlap(_uri, DEFAULT_URI_PARAMS)
    else:
        raise RuntimeError(
            f"uri: {uri} type: {uri.__class__} is not supported"
        )

    overlap(_uri, kw)

    if _uri.setdefault("path", "/")[:1] != "/":
        _uri["path"] = f"/{_uri['path']}"

    return _uri


def complete_duri(uri: URI | QUERY, _ignore_cache_=False, **kw) -> QUERY:
    _uri = parse_duri(uri, _ignore_cache_=_ignore_cache_)
    uri = build_uri(**_uri)
    return uri


# ---------------------------------------------------------
# Basic iCRUD proposal
# ---------------------------------------------------------
class iConnection:
    def create(self, thing, data, record_id=None):
        raise NotImplementedError()

    def update(self, thing, data, record_id=None):
        raise NotImplementedError()

    def query(self, thing, data, record_id=None):
        raise NotImplementedError()

    def select(self, thing, data, record_id=None):
        raise NotImplementedError()

    def use(self, namespace, database):
        raise NotImplementedError()


class iCRUD:

    async def get(self, uri: URI):
        "Get an object from URI"
        raise NotImplementedError()

    async def put(self, uri: URI, data: JSON = None, **kw) -> bool:
        "Put an object from URI"
        raise NotImplementedError()

    async def update(self, uri: URI, data: JSON = None, **kw) -> bool:
        "Update an object from URI"
        raise NotImplementedError()

    async def delete(self, uri: URI):
        "Delete an object from URI"
        raise NotImplementedError()

    async def query(self, query: URI | QUERY) -> List[JSON]:
        "Make a query to the system based on URI (pattern)"
        raise NotImplementedError()


class iPolicy:
    "base of criteria / policies"
    DISCARD = "discard"
    STORE = "store"

    def __init__(self, storage):
        self.storage = storage

    async def action(self, mode, thing, data):
        return self.STORE


class iStorage(iCRUD):

    def __init__(self, url, policy=iPolicy):
        super().__init__()
        self.url = url
        self.policy = policy(storage=self)
        # self.connection = None
        self.connections = {}
        self._last_connection = None

    async def live(self, uri: URI) -> JSON:
        "Make a live query to the system based on URI (pattern)"
        raise NotImplementedError()

    def running(self):
        return 0

    async def save(self, nice=False, wait=False):
        "TBD"
        raise NotImplementedError()

    async def _prepare_call(self, uri):
        _uri = parse_duri(uri)
        # mapping to surreal
        namespace = tf(_uri.get("fscheme", DEFAULT_NAMESPACE))
        database = tf(_uri.get("host", DEFAULT_DATABASE))
        _path = _uri.get("_path")
        if not _path:
            # need to guess table / id from id
            uid = _uri["id"]  # must exists
            m = REG_SPLIT_PATH.match(uid)
            if m:
                _uri.update(m.groupdict())
            thing = tf(_uri["_path"])
        else:
            thing = tf(_path)
        # surreal special chars: ⟨ ⟩
        # tube mode
        key = namespace, database
        connection = self.connections.get(key) or await self._connect(*key)
        assert connection, f"{self} get connection has failed"

        return connection, thing, _uri

    async def _connect(self, *key) -> iConnection:
        raise NotImplementedError()

    async def put(self, uri: URI, data: JSON = None, **kw) -> bool:
        if data is None:
            data = kw
        else:
            data.update(kw)

        try:
            connection, thing, _uri = await self._prepare_call(uri)
            record_id = _uri["id"] or data.get("id", None)  # must exists!
            record_id = tf(record_id)
            record_id = esc(record_id)
            if record_id:
                data = data.copy()
                data.pop(
                    "id", None
                )  # can't use record_id and data['id]. It'll fail in silence
                result = connection.update(thing, data, record_id=record_id)
            else:
                result = connection.create(thing, data)

            return result.result and result.status in (
                "OK",
                STATUS_OK,
            )  # True|False

        except Exception as why:
            log.error(why)
            log.error("".join(traceback.format_exception(*sys.exc_info())))

    async def update(
        self, query: URI | QUERY, data: JSON = None, **kw
    ) -> List[JSON]:
        "Update object from URI"
        if data is None:
            data = kw
        else:
            data.update(kw)

        record_id = data.get("id", None)
        if record_id:
            # update single record
            conn, table, _uri = await self._prepare_call(query)
            record_id = esc(record_id)
            result = conn.update(record_id, data)
        else:
            # update many
            stream = await self.query(query)
            conn = self._last_connection  # reuse exact same connection
            for _data in stream:
                _data.update(data)

                m = REG_SPLIT_PATH.match(_data["id"])
                d = m.groupdict()
                table = d["_path"]
                result = conn.update(table, _data)

        return result.result and result.status in ("OK",)  # True|False

    async def get(self, uri: URI, cache=True) -> JSON:
        try:
            conn, table, _uri = await self._prepare_call(uri)
            record_id = _uri["id"]
            record_id = esc(record_id)
            res = conn.select(record_id)
            result = res.result
            if result:
                data = result[0]
        except Exception as why:
            log.warning(why)

        return data
