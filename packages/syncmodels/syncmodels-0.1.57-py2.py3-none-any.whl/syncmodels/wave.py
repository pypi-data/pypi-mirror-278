import random
from typing import Dict, List

from agptools.helpers import build_uri, parse_xuri


from .definitions import UID, WAVE, JSON, MONOTONIC_KEY, URI
from .crud import iStorage, parse_duri, tf

# TODO: check https://pypi.org/project/speedict/
# TODO: check https://github.com/speedb-io/python-speedb
# TODO: check https://github.com/grantjenks/python-diskcache/tree/master
# TODO: check https://github.com/unum-cloud/ustore

TUBE_NS = "system"
TUBE_DB = "swarmtube"
TUBE_META = "TubeMeta"
TUBE_WAVE = "TubeWave"
TUBE_SYNC = "TubeSync"


def get_tube_name(klass):
    if isinstance(klass, str):
        tube_name = klass.split(":")[-1]
    else:
        tube_name = f"{klass.__module__.replace('.', '_')}_{klass.__name__}"
    return tube_name


class iWaves:
    """Swarm Flows / Waves storage.
    Base implementation is for Surreal, but can be
    overridden by sub-classing
    """

    MODE_SNAPSHOT = "snap"
    MODE_TUBE = "tube"

    MAX_HARD_CACHE = 120
    MAX_SOFT_CACHE = 100

    TUBE_SYNC_WAVES = {}

    def __init__(self, storage: iStorage, *args, **kw):
        super().__init__(*args, **kw)
        self.cache = {}
        self.storage = storage

    async def last_wave(self, target: URI) -> WAVE:
        "return the last wave of an object"
        # TODO: use uri and current namespace / database
        _uri = parse_duri(target)
        # just for clarity
        namespace = _uri["fscheme"]
        database = _uri["host"]
        tube_name = _uri["_path"]
        # tube_name = get_tube_name(klass)
        tube_name = tf(tube_name)
        query = f'{namespace}://{database}/{TUBE_WAVE}?id={TUBE_WAVE}:{tube_name}'
        result = await self.storage.query(query)
        return result
        # TODO: use URI instead!!

    async def update_sync_wave(
        self, sources: List[URI], target: URI, wave: WAVE
    ):
        """Update the synchronization wave
        of some sources for a particular target
        """
        wave = int(wave)
        record = {
            "target": target,
            MONOTONIC_KEY: wave,
        }

        results = []
        for source in sources:

            query = f'{TUBE_NS}://{TUBE_DB}/{TUBE_SYNC}?source={source}&target={target}'
            # Note that record hasn't `id`, we need to find if the
            # record already exist or is new one
            _results = await self.storage.query(query)
            if _results:
                record = _results[0]
                record[MONOTONIC_KEY] = wave
                result = await self.storage.update(query, record)
            else:
                record['source'] = source
                result = await self.storage.put(query, record)

            results.append(result)
        return all(results)

    async def last_waves(
        self, sources: List[URI], target: URI
    ) -> Dict[URI, WAVE]:
        "return the last wave of an object"
        _uri = parse_duri(target)
        # just for clarity
        namespace = _uri["fscheme"]
        database = _uri["host"]

        waves = {}
        for source in sources:
            query = f'{namespace}://{database}/{TUBE_SYNC}?source={source}&target={target}'
            result = await self.storage.query(query)
            if result:
                waves[source] = result[0][MONOTONIC_KEY]
            else:
                waves[source] = 0
        return waves

    async def since(self, fqid, wave, max_results=100):
        "return the last objects since a wave"
        # TODO: use URI instead!!

    def _has_change(self, uri: UID, **data: JSON):
        # TODO: ask to TUBE_WAVE instead (direct check by id)
        _uri = parse_duri(uri)
        if data:
            root = self.cache
            for key in _uri['_path'].split('/'):
                root = root.setdefault(key, {})
            current = root.get(uid := _uri['id'])
            if current != data:
                # check cache size
                if len(root) > self.MAX_HARD_CACHE:
                    keys = list(root.keys())
                    while (l := len(keys)) > self.MAX_SOFT_CACHE:
                        k = random.randint(0, l - 1)
                        root.pop(keys.pop(k))

                root[uid] = data
                return True
        return False

    async def start(self):
        "any action related to start storage operations"

    async def stop(self):
        "any action related to stop storage operations"

    async def update_meta(self, tube, meta, merge=True):
        """Update the tube metadata.
        If merge is True, meta-data will me merge
        If merge is False, meta-data will be replace
        """

    async def find_meta(self, meta):
        """Find tubes that match the specified meta"""
        return []

    async def save(self, nice=False, wait=False):
        return await self.storage.save(nice, wait)
