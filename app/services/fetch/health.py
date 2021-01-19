import asyncio

from services.fetch.base import BaseFetcher
from services.lib.depcont import DepContainer
from services.models.health import BridgeHealth


class HealthFetcher(BaseFetcher):
    def __init__(self, deps: DepContainer):
        sleep_period = deps.cfg.bridge.eth.period
        super().__init__(deps, sleep_period)
        self.eth_api_url = deps.cfg.bridge.eth.api

    def stats_url(self):
        return f"{self.eth_api_url}/stats"

    def main_url(self):
        return f"{self.eth_api_url}/"

    async def fetch_main(self):
        session = self.deps.session
        async with session.get(self.main_url()) as resp:
            main_json = await resp.json()
            return main_json

    async def fetch_stats(self):
        session = self.deps.session
        async with session.get(self.stats_url()) as resp:
            j = await resp.json()
            return j

    async def fetch(self):
        main_json, stats_json = await asyncio.gather(self.fetch_main(), self.fetch_stats())
        data = BridgeHealth.from_jsons(main_json, stats_json)
        return data
