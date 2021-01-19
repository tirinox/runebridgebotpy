import logging

from localization import BaseLocalization
from services.fetch.base import INotified
from services.lib.depcont import DepContainer


class CapFetcherNotifier(INotified):
    def __init__(self, deps: DepContainer):
        self.deps = deps
        self.logger = logging.getLogger('CapFetcherNotification')

    async def on_data(self, sender, data):
        ...
