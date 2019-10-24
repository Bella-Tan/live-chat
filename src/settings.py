import os

__mode__ = "Anonymous"


class Settings:

    @staticmethod
    def get_mode():
        return __mode__

    @staticmethod
    def set_mode(setting):
        __mode__ = setting

