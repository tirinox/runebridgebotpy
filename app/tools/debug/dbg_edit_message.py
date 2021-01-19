from main import App


class TestApp1(App):
    async def _run_background_jobs(self):
        users = await self.deps.broadcaster.all_users()
        me = users[0]
        bot = self.deps.bot
        message = await bot.send_message(me, 'test')
        ident = message.message_id
        await bot.edit_message_text('edited', me, message_id=ident)



if __name__ == '__main__':
    print('-' * 100)
    TestApp1().run_bot()
