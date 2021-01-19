import logging

from services.lib.depcont import DepContainer
from services.models.job import JobTxInfo


class JobStatusNotifier:
    def __init__(self, deps: DepContainer):
        self.deps = deps
        self.logger = logging.getLogger('JobStatusNotifier')

    async def notify_new_job(self, job: JobTxInfo):
        # 1. if not completed => register message for editing
        # 2. if completed => remove
        ...

    async def edit_job(self, job: JobTxInfo):
        # 1.
        ...