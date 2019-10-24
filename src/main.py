import tornado.ioloop
from handlers.foo import Application
from utils.logger import Logger
from tornado.options import define, options
from settings import Settings

logger = Logger.get_logger(__name__)

define("mode", default="Normal", help="Normal or Anonymous")

if __name__ == "__main__":
    options.parse_command_line()
    Settings.set_mode(options.mode)
    app = Application()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
