import asyncio
import logging
from typing import List

from services.fetch.base import INotified
from services.lib.depcont import DepContainer
from services.models.job import JobTxInfo
from services.notify.types.job_notify import JobStatusNotifier


class JobsProcessor(INotified):
    def __init__(self, deps: DepContainer):
        self.deps = deps
        self.logger = logging.getLogger('JobsProcessor')
        self.prev_jobs = {}
        self.notifier = JobStatusNotifier(deps)
        self.once_observed = set()

    async def on_data(self, sender, data: List[JobTxInfo]):
        fresh_jobs = {j.ident: j for j in data}
        fresh_jobs_ids = set(fresh_jobs.keys())

        if not self.prev_jobs:
            # first call: only observe what was before and return
            self.prev_jobs = fresh_jobs
            self.once_observed.update(fresh_jobs_ids)
            return

        prev_jobs_ids = set(self.prev_jobs.keys())

        # jobs that post a new message
        jobs_added_ids = fresh_jobs_ids - prev_jobs_ids - self.once_observed
        self.once_observed.update(fresh_jobs_ids)

        # jobs that edit previous message
        jobs_old_ids = fresh_jobs_ids & prev_jobs_ids  # intersection
        jobs_update_ids = set()
        for job_id in jobs_old_ids:
            current_job: JobTxInfo = fresh_jobs[job_id]
            old_job: JobTxInfo = self.prev_jobs[job_id]
            # if status is changed
            if current_job.status != old_job.status:
                jobs_update_ids.add(job_id)

        await self._notify_all(fresh_jobs, jobs_added_ids, jobs_update_ids)

        self.prev_jobs = fresh_jobs  # swap buffers!

    async def _notify_all(self, fresh_jobs, jobs_added_ids, jobs_update_ids):
        await self.notifier.update_users()
        for job_id in jobs_added_ids:
            asyncio.create_task(self.notifier.notify_new_job(fresh_jobs[job_id]))
        for job_id in jobs_update_ids:
            asyncio.create_task(self.notifier.edit_job(fresh_jobs[job_id]))
