import json
import os

from dataclasses_serialization.json import JSONSerializer

from services.fetch.base import BaseFetcher
from services.lib.depcont import DepContainer
from services.lib.utils import async_wrap
from services.models.job import JobTxInfo


class BridgeJobsFetcher(BaseFetcher):
    def __init__(self, deps: DepContainer):
        sleep_period = deps.cfg.bridge.eth.jobs.period
        super().__init__(deps, sleep_period)
        self.eth_api_url = deps.cfg.bridge.eth.api

    def jobs_url(self):
        return f"{self.eth_api_url}/jobs"

    async def fetch(self):
        try:
            async with self.deps.session.get(self.jobs_url()) as resp:
                data = await resp.json()
                jobs = data['jobs']
                return [JobTxInfo.from_api_json(j) for j in jobs]
        except Exception:
            self.logger.exception('Could not connect to API or parse error', exc_info=True)
            return []


class MockBridgeJobsFetcher(BridgeJobsFetcher):
    """
    Use this to test notification on the real world data without doing any real TX
    """
    RECORDED_DIR = 'tools/recorded_jobs'

    def __init__(self, deps: DepContainer, path=None):
        super().__init__(deps)
        self.logger.warning('using fake jobs fetcher!')
        self.path = path or self.RECORDED_DIR
        self.files = [f for f in sorted(os.listdir(self.path)) if f.startswith('jobs-') and f.endswith('.json')]
        self.files = [os.path.join(self.path, f) for f in self.files]
        self.counter = 0

    @async_wrap
    def read_file(self, i):
        assert self.files

        if i >= len(self.files):
            self.logger.warning('mock jobs are over. using the last one forever...')
            i = len(self.files) - 1

        with open(self.files[i], 'r') as file:
            jobs_raw_arr = json.load(file)
            jobs = [JSONSerializer.deserialize(JobTxInfo, item) for item in jobs_raw_arr]

            self.logger.info(f'mock job was read: {self.files[i]} ({len(jobs)}) jobs loaded.')
            return jobs

    async def fetch(self):
        jobs = await self.read_file(self.counter)
        self.counter += 1
        return jobs
