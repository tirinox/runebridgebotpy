from aiogram.types import *

from services.dialog.base import BaseDialog, message_handler


class MainMenuDialog(BaseDialog):
    @message_handler(commands='start,lang', state='*')
    async def entry_point(self, message: Message):
        await message.answer('heeloll')

