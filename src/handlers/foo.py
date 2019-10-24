import tornado.ioloop
import json
import tornado.web
from tornado.routing import HostMatches
from tornado.websocket import WebSocketHandler
from utils.logger import Logger
from handlers.base import BaseHandler
from services.chat import ChatService

logger = Logger.get_logger(__name__)


class HomeHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render('home.html')


class ChatHandler(WebSocketHandler):
    def open(self):
        # login
        print("on_open")
        channel = self.get_argument("channel")
        username = self.get_argument("userName")
        role = self.get_argument("role")
        message = ChatService.register(channel, username, role, self)
        self.write_message(json.dumps(message))
        logger.info("chat connection received from {0}".format(username))

    def on_close(self):
        # logout
        print("on_close")
        logger.info("chat connection closing")

    def error_msg(self, error_code):
        if error_code is not None:
            logger.error("send failed, error code :%s", str(error_code))
            json_string = json.dumps({"type": "error", "code": error_code})
            # self.set_header("Content-Type", "application/json")
            self.write_message("{0}".format(json_string))
        else:
            logger.error("invalid error code")

    def on_message(self, message):
        # channel id、user id、content
        print("on_message", str(message))

        msg = json.loads(message)
        channel = msg["channel"]
        user_id = msg["user_id"]
        msg_type = msg["type"]
        if msg_type == "exit":
            ChatService.unregister(channel, user_id)
        elif msg_type == "msg":
            msg_ts = msg["ts"]
            content = msg["msg"]
            ChatService.news(channel, user_id, msg_ts, content)


class ChannelHandler(BaseHandler):
    def get(self, *args, **kwargs):
        arguments = self.get_arguments()
        channel = arguments["channel"]
        user_name = arguments["userName"]
        role = arguments["role"]
        # self.redirect('/channel?channel=%s&userName=%s&role=%s' % (channel, user_name, role))
        self.render('channel.html', channel=channel, userName=user_name, role=role)


class Application(tornado.web.Application):
    def __init__(self):
        settings = {
            'template_path': 'html',
            'static_path': 'static'
        }

        tornado.web.Application.__init__(self, [
            (HostMatches("localhost"), [
                (r"/", HomeHandler),
                # (r"/redirect", RedirectHandler),
                (r"/channel", ChannelHandler),
                (r"/channel/chat", ChatHandler),
            ]),
        ], **settings)
