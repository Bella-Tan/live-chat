import threading

"""
    lock on class method while the class has lock attribute
"""


def synchronized(attr):
    def decorator(method):
        def synced_method(self, *args, **kws):
            if not hasattr(self, attr):
                setattr(self, attr, threading.RLock())
            lock = getattr(self, attr)
            with lock:
                return method(self, *args, **kws)

        return synced_method

    return decorator
