from services.lib.db import DB


class MessageTracker:
    def __init__(self, db: DB):
        self.db = db

    @staticmethod
    def key(item_hash):
        return f'msg_track:{item_hash!s}'

    async def add_message_for_item(self, item_hash: str, chat_id: int, message_id: int):
        if not item_hash:
            return
        redis = await self.db.get_redis()
        return await redis.hset(self.key(item_hash), str(chat_id), str(message_id))

    async def remove_all_msg_of_item(self, item_hash: str):
        if not item_hash:
            return
        redis = await self.db.get_redis()
        return await redis.delete(key=self.key(item_hash))

    async def get_all(self, item_hash: str):
        if not item_hash:
            return
        redis = await self.db.get_redis()
        items = await redis.hgetall(self.key(item_hash))
        return [(int(k), int(v)) for k, v in items.items()]

