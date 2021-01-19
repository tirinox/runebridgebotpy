import logging

from services.fetch.base import INotified
from services.lib.depcont import DepContainer
from services.models.health import BridgeHealth


class HealthNotifier(INotified):
    def __init__(self, deps: DepContainer):
        self.deps = deps
        self.logger = logging.getLogger('HealthNotifier')

    async def on_data(self, sender, data: BridgeHealth):
        if data.status != data.STATUS_LIVE:
            users = await self.deps.broadcaster.all_users()
            await self.deps.broadcaster.broadcast(users, f'{data}')
