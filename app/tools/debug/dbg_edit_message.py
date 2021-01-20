import asyncio

from main import App
from services.models.msg_track import MessageTracker


class TestApp1(App):
    async def _simple_edit_message(self):
        users = await self.deps.broadcaster.all_users()
        me = users[0]
        bot = self.deps.bot
        message = await bot.send_message(me, 'test')
        ident = message.message_id
        await asyncio.sleep(1.0)
        # edit message having chat_id and message_id
        await bot.edit_message_text('edited', me, message_id=ident)

    async def _test_msg_tracker(self):
        tr = MessageTracker(self.deps.db)
        hash1 = '0x1234aBBa6789'
        await tr.add_message_for_item(hash1, 100, 66)
        await tr.add_message_for_item(hash1, 101, 55)
        await tr.add_message_for_item(hash1, 102, 44)

        items = await tr.get_all(hash1)
        print(items)
        print('--' * 100)

        await tr.remove_all_msg_of_item(hash1)
        items = await tr.get_all(hash1)
        print(items)
        print('--' * 100)

        exit(0)


    async def _run_background_jobs(self):
        # await self._simple_edit_message()
        await self._test_msg_tracker()


if __name__ == '__main__':
    print('-' * 100)
    TestApp1().run_bot()
