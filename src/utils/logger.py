import logging
import sys
logging.getLogger("tornado.access").disabled = True
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="[%(asctime)s] [MSG] [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s"
)


class Logger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)

    def error(self, msg, ctx=None, e=None):
        self.logger.error("CAUSE=%s, CONTEXT=%s, EXCEPTION=%s", e, ctx, msg)

    def debug(self, msg, ctx=None, e=None):
        self.logger.debug("CAUSE=%s, CONTEXT=%s, EXCEPTION=%s", e, ctx, msg)

    def info(self, msg, ctx=None):
        self.logger.info("%s, CONTEXT=%s", msg, ctx)

    @staticmethod
    def get_logger(name):
        return Logger(name).logger
