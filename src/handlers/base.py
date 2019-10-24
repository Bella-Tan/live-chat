import json
import tornado.web
from utils.logger import Logger

logger = Logger.get_logger(__name__)


class BaseHandler(tornado.web.RequestHandler):

    def data_received(self, chunk):
        pass

    def get_arguments(self):
        try:
            return dict({k: self.get_argument(k) for k in self.request.arguments})
        except Exception:
            msg = "Some arguments are in bad format. Please validate and try again."
            logger.error(msg)
            raise tornado.web.HTTPError(400, msg)

    def write_error(self, status_code, **kwargs):
        if "exc_info" in kwargs:
            # self.set_header("Content-Type", "application/json")
            self.set_status(status_code)
            exc_info = kwargs["exc_info"]
            for e in exc_info:
                if type(e) is tornado.web.HTTPError:
                    e = tornado.web.HTTPError(e).status_code
                    self.finish(
                        "{\"errorMessage\":\"%s\", \"errorCode\":%d, \"errorDetail\":\"%s\"}"
                        % (e.log_message, e.status_code, e.reason))
                    return
        else:
            # self.set_header("Content-Type", "application/json")
            self.set_status(status_code)
            self.finish(str(status_code))
