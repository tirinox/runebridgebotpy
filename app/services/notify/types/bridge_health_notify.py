import logging

from localization import BaseLocalization
from services.fetch.base import INotified
from services.lib.depcont import DepContainer
from services.notify.broadcast import Broadcaster


class HealthNotifier(INotified):
    def __init__(self, deps: DepContainer):
        self.deps = deps
        self.logger = logging.getLogger('HealthNotifier')

    async def on_data(self, sender, data):
        users = await self.deps.broadcaster.all_users()
        await self.deps.broadcaster.broadcast(users, 'test')
