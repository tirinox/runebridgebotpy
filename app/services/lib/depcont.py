import typing
import asyncio
from dataclasses import dataclass

from aiogram import Bot, Dispatcher
from aiohttp import ClientSession


# noinspection PyUnresolvedReferences
@dataclass
class DepContainer:
    cfg: typing.Optional['Config'] = None
    db: typing.Optional['DB'] = None
    loop: typing.Optional[asyncio.BaseEventLoop] = None

    session: typing.Optional[ClientSession] = None

    bot: typing.Optional['Bot'] = None
    dp: typing.Optional['Dispatcher'] = None
    loc_man: typing.Optional['LocalizationManager'] = None

    broadcaster: typing.Optional['Broadcaster'] = None

    health_fetch: typing.Optional['HealthFetcher'] = None
    job_fetch: typing.Optional['BridgeJobsFetcher'] = None

