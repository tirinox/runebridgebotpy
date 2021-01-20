import asyncio
import json
import logging
import os

import aiohttp
from dataclasses_serialization.json import JSONSerializer

from services.fetch.jobs import BridgeJobsFetcher
from services.lib import datetime
from services.lib.config import Config
from services.lib.db import DB
from services.lib.depcont import DepContainer
from services.lib.utils import async_wrap

d = DepContainer()
d.cfg = Config()

log_level = d.cfg.get('log_level', logging.INFO)
logging.basicConfig(
    level=logging.getLevelName(log_level),
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

logging.info(f"Log level: {log_level}")

d.loop = asyncio.get_event_loop()
d.db = DB(d.loop)

job_fetch = BridgeJobsFetcher(d)


@async_wrap
def save_jobs(jobs):
    date_str = datetime.datetime.now().isoformat()
    name = os.path.join('tools', 'recorded_jobs', f"jobs-{date_str}.json")
    with open(name, 'w') as f:
        serialized_jobs = JSONSerializer.serialize(jobs)
        json.dump(serialized_jobs, f)
        logging.info(f'[{name}] dumped {len(serialized_jobs)} jobs.')


async def main():
    previous_jobs = None
    async with aiohttp.ClientSession() as d.session:
        while True:
            await asyncio.sleep(3.0)

            jobs = await job_fetch.fetch()
            if not jobs:
                logging.warning('no jobs fetched!')
                continue

            if previous_jobs is not None:
                if previous_jobs != jobs:
                    await save_jobs(jobs)
                else:
                    logging.info('no changes. sleeping...')
            else:
                logging.info('init first jobs package!')
                await save_jobs(jobs)

            previous_jobs = jobs


asyncio.run(main())
