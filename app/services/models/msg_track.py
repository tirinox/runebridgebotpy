from services.lib.db import DB

# 1. store chat_id + message_id.

class MessageTracker:
    def __init__(self, db: DB):
        self.db = db

