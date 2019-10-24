import threading

from settings import Settings
from models.channel import Channel

_MODE = Settings.get_mode()


class ChatService(object):
    channels = {}
    lock = threading.Lock()

    @classmethod
    def register(cls, channel_id, name, role, handler):
        with cls.lock:
            if channel_id not in cls.channels.keys():
                cls.channels[channel_id] = Channel(channel_id)
            channel = cls.channels[channel_id]
            return channel.add_user(name, role, handler)

    @classmethod
    def unregister(cls, channel_id, user_id):
        with cls.lock:
            if channel_id in cls.channels.keys():
                cls.channels[channel_id].del_user(user_id)
            if cls.channels[channel_id].user_count() == 0:
                del cls.channels[channel_id]

    @classmethod
    def news(cls, channel_id, user_id, ts, content):
        with cls.lock:
            if channel_id not in cls.channels.keys():
                return {"type": "error", "reason": "invalid channel id"}
            cls.channels[channel_id].add_message(user_id, ts, content)
            return None
