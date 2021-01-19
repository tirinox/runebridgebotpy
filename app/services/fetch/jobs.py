import asyncio

from services.fetch.base import BaseFetcher
from services.lib.depcont import DepContainer
from services.models.health import BridgeHealth
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

    # todo: filter old TX return only fresh and updated TX!
