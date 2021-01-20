import logging

from localization import BaseLocalization
from services.fetch.base import INotified
from services.lib.depcont import DepContainer
from services.models.health import BridgeHealth


class HealthNotifier(INotified):
    def __init__(self, deps: DepContainer):
        self.deps = deps
        self.logger = logging.getLogger('HealthNotifier')
        self.last_status = None

    KEY_LAST_STATUS = 'bridge_last_status'

    async def get_old_status(self):
        redis = await self.deps.db.get_redis()
        if self.last_status is None:
            last_status = (await redis.get(self.KEY_LAST_STATUS))
            if last_status is None:
                last_status = BridgeHealth.STATUS_OFFLINE
            else:
                last_status = last_status.decode()
            self.last_status = last_status
        return self.last_status

    async def on_data(self, sender, data: BridgeHealth):
        self.last_status = await self.get_old_status()

        if data.status != self.last_status:
            self.last_status = data.status

            redis = await self.deps.db.get_redis()
            await redis.set(self.KEY_LAST_STATUS, data.status)

            users = await self.deps.broadcaster.all_users()
            loc: BaseLocalization = self.deps.loc_man.default
            await self.deps.broadcaster.broadcast(users, loc.current_info(data))
