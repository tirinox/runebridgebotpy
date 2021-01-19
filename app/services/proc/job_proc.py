import logging
from typing import List

from services.fetch.base import INotified
from services.lib.depcont import DepContainer
from services.models.job import JobTxInfo


class JobsProcessor(INotified):
    def __init__(self, deps: DepContainer):
        self.deps = deps
        self.logger = logging.getLogger('JobsProcessor')

    async def on_data(self, sender, jobs: List[JobTxInfo]):
        print(jobs[1])
        # 1. filter out completed (local)
        # 2. detect new jobs
        # 3. send messages for new jobs and memorize their (chat_it, message_it)
        # 4. update messages with changed status
        # 5. if job completed => remove it from the list of saved messages
        ...
