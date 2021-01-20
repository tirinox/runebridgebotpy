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

    async def on_data(self, sender, data: List[JobTxInfo]):
        fresh_jobs = {j.ident: j for j in data}
        if not self.prev_jobs:
            self.prev_jobs = fresh_jobs
            return

        fresh_jobs_ids = set(fresh_jobs.keys())
        prev_jobs_ids = set(self.prev_jobs.keys())
        jobs_added_ids = fresh_jobs_ids - prev_jobs_ids
        jobs_old_ids = fresh_jobs_ids & prev_jobs_ids  # intersection

        jobs_update_ids = set()
        for job_id in jobs_old_ids:
            current_job: JobTxInfo = fresh_jobs[job_id]
            old_job: JobTxInfo = self.prev_jobs[job_id]
            if current_job.status != old_job.status:
                jobs_update_ids.add(job_id)

        for job_id in jobs_added_ids:
            await self.notifier.notify_new_job(fresh_jobs[job_id])

        for job_id in jobs_update_ids:
            await self.notifier.edit_job(fresh_jobs[job_id])

        self.prev_jobs = fresh_jobs  # swap buffers!
