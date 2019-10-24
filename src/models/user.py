from uuid import uuid4


class User:

    def __init__(self, name, role, handler):
        self.uid = str(uuid4())
        self.name = name
        self.role = role
        self.handler = handler

    def get_user_info(self):
        return {
            "userid": self.uid,
            "name": self.name,
            "role": self.role
        }

    def get_role(self):
        return self.role

    def get_name(self):
        return self.name

    def get_user_id(self):
        return self.uid

    def get_handler(self):
        return self.handler
