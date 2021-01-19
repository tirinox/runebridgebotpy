import asyncio
import logging
import os

import aiohttp
import ujson
from aiogram import Bot, Dispatcher, executor
from aiogram.types import *

from localization import LocalizationManager
from services.dialog import init_dialogs
from services.lib.config import Config
from services.lib.db import DB
from services.lib.depcont import DepContainer
from services.notify.broadcast import Broadcaster
from services.notify.types.bridge_notify import CapFetcherNotifier


class App:
    def __init__(self):
        d = self.deps = DepContainer()
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

    def create_bot_stuff(self):
        d = self.deps

        d.bot = Bot(token=d.cfg.telegram.bot.token, parse_mode=ParseMode.HTML)
        d.dp = Dispatcher(d.bot, loop=d.loop)
        d.loc_man = LocalizationManager()
        d.broadcaster = Broadcaster(d)

        init_dialogs(d)

    async def connect_chat_storage(self):
        if self.deps.dp:
            self.deps.dp.storage = await self.deps.db.get_storage()


    async def _run_background_jobs(self):
        d = self.deps

        # fetcher_cap = CapInfoFetcher(d, ppf=self.ppf)
        # fetcher_cap.subscribe(notifier_cap)

        await asyncio.gather(*(task.run() for task in [
            # fetcher_cap,
        ]))

    async def on_startup(self, _):
        await self.connect_chat_storage()

        self.deps.session = aiohttp.ClientSession(json_serialize=ujson.dumps)
        asyncio.create_task(self._run_background_jobs())

    async def on_shutdown(self, _):
        await self.deps.session.close()

    def run_bot(self):
        self.create_bot_stuff()
        executor.start_polling(self.deps.dp, skip_updates=True, on_startup=self.on_startup,
                               on_shutdown=self.on_shutdown)


if __name__ == '__main__':
    print('-' * 100)
    App().run_bot()