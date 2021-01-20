import logging

from aiogram.types import Message

from localization import BaseLocalization
from services.lib.depcont import DepContainer
from services.lib.texts import MessageType
from services.models.job import JobTxInfo
from services.models.msg_track import MessageTracker
from services.notify.broadcast import Broadcaster


class JobStatusNotifier:
    def __init__(self, deps: DepContainer):
        self.deps = deps
        self.logger = logging.getLogger('JobStatusNotifier')
        self.tracker = MessageTracker(deps.db)
        self.users = []
        self.loc: BaseLocalization = self.deps.loc_man.default  # todo?

    async def update_users(self):
        self.users = await self.deps.broadcaster.all_users()

    async def notify_new_job(self, job: JobTxInfo):
        self.logger.info(f'new job detected: {job}')

        tr = self.tracker
        br: Broadcaster = self.deps.broadcaster

        message = self.loc.tx_alert_text(job)
        all_messages = await br.broadcast(self.users, message, message_type=MessageType.TEXT)
        if job.is_completed:
            await tr.remove_all_msg_of_item(job.ident)
        else:
            for message in all_messages:
                if isinstance(message, Message):
                    await tr.add_message_for_item(job.ident, message.chat.id, message.message_id)

    async def edit_job(self, job: JobTxInfo):
        self.logger.info(f'edit job: {job}')

        tr = self.tracker
        br: Broadcaster = self.deps.broadcaster

        message = self.loc.tx_alert_text(job)

        all_messages = await tr.get_all(job.ident)

        await br.broadcast(all_messages, message, message_type=MessageType.EDIT_TEXT,
                           shuffle_chats=False,
                           disable_web_page_preview=True)

        if job.is_completed:
            await tr.remove_all_msg_of_item(job.ident)
