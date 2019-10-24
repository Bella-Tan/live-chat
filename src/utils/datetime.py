from datetime import datetime


class Time:
    @staticmethod
    def now():
        return str(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S %Z"))
