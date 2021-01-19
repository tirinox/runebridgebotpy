from services.fetch.base import BaseFetcher
from services.lib.depcont import DepContainer


class HealthFetcher(BaseFetcher):
    def __init__(self, deps: DepContainer):
        sleep_period = deps.cfg.bridge.eth.period
        super().__init__(deps, sleep_period)
        self.eth_api_url = deps.cfg.bridge.eth.api

    async def fetch(self):
        return True
