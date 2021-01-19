from aiogram.types import *

from services.dialog.base import BaseDialog, message_handler


class MainMenuDialog(BaseDialog):
    @message_handler(commands='start,lang', state='*')
    async def entry_point(self, message: Message):
        await self.deps.broadcaster.register_user(message.from_user.id)
        await message.answer('Hello!')

    @message_handler(commands='info', state='*')
    async def info_command(self, message: Message):
        info = await self.deps.health_fetch.fetch()
        await message.answer(self.loc.current_info(info),
                             disable_notification=True,
                             disable_web_page_preview=True)

    @message_handler(commands='stop', state='*')
    async def stop_command(self, message: Message):
        await message.answer('You unsubscribed. Use /start to resubscribe.')
        await self.deps.broadcaster.remove_users([message.from_user.id])
