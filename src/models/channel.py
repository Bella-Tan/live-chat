import json

from models.user import User
from utils.datetime import Time
from utils.decorator import synchronized

roles = {"instructor": "Instructor", "student": "Student"}


class Channel:
    def __init__(self, channel_id):
        self.mode = "normal"
        self.messages = []
        self.id = channel_id
        self.users = {}

    def __notify_in_channel(self, from_uid, normal_msg, anonymity_msg):
        for k in self.users:
            if k != from_uid:
                # self.users[k].get_handler().set_header("Content-Type", "application/json")
                if self.users[k].get_role() == "Instructor":
                    self.users[k].get_handler().write_message(json.dumps(normal_msg))
                else:
                    self.users[k].get_handler().write_message(json.dumps(anonymity_msg))

    def __sync_user_list(self):
        message = {"channel": self.id, "type": "userlist", "userlist": []}
        anonymity_message = {"channel": self.id, "type": "userlist", "userlist": []}
        for user_id in self.users:
            message["userlist"].append(
                {"userid": user_id, "name": self.users[user_id].get_name(), "role": self.users[user_id].get_role()})
            anonymity_message["userlist"].append(
                {"userid": 0, "name": "anonymity", "role": self.users[user_id].get_role()})

        length = len(message["userlist"])
        for i in range(length):
            user = message["userlist"].pop(i)
            self.__notify_in_channel(user["userid"], message, anonymity_message)
            message["userlist"].append(user)

        return message

    @synchronized("lock")
    def add_user(self, name, role, handler):
        user = User(name, role, handler)
        self.users[user.get_user_id()] = user

        time_now = Time.now()
        notify_msg = {"channel": self.id, "type": "notification",
                      "notification": '%s join channel at %s' % (name, time_now)}
        anonymity_notify_msg = {"channel": self.id, "type": "notification",
                                "notification": '%s join channel at %s' % ("anonymity", time_now)}
        self.__notify_in_channel(user.get_user_id(), notify_msg, anonymity_notify_msg)
        self.__sync_user_list()
        return {"channel": self.get_id(), "type": "user_id", "user_id": user.get_user_id()}

    @synchronized("lock")
    def del_user(self, user_id):
        time_now = Time.now()
        name = self.users[user_id].get_name()
        notify_msg = {"channel": self.id, "type": "notification",
                      "notification": '%s leave channel at %s' % (name, time_now)}
        anonymity_notify_msg = {"channel": self.id, "type": "notification",
                                "notification": '%s leave channel at %s' % ("anonymity", time_now)}
        self.__notify_in_channel(user_id, notify_msg, anonymity_notify_msg)
        del self.users[user_id]
        self.__sync_user_list()

    @synchronized("lock")
    def user_count(self):
        return len(self.users)

    def get_id(self):
        return self.id

    @synchronized("lock")
    def add_message(self, user_id, ts, content):
        message = {"channel": self.id, "type": "msg",
                   "msg": {"fromname": self.users[str(user_id)].get_name(), "fromid": str(user_id),
                           "content": content, "ts": ts}}
        anonymity_message = {"channel": self.id, "type": "msg", "msg": {"fromname": "anonymity", "fromid": str(0),
                                                                        "content": content}}
        self.__notify_in_channel(str(user_id), message, anonymity_message)
        message["ts"] = ts
        self.messages.append(message)

    @synchronized("lock")
    def get_history_message(self, b_ts, e_ts):
        collect_message = []
        for _, msg in enumerate(self.messages):
            if b_ts <= msg["ts"] >= e_ts:
                tmp_msg = msg.copy()
                del tmp_msg["ts"]
                collect_message.append(tmp_msg)
        return collect_message
