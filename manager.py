import requests
from requests import utils


class User:
    def __init__(self, username: str, cookies: map, session: requests.Session):
        self.name = username
        self.cookies = cookies
        self.session = session

    def update(self):
        self.cookies = self.session.cookies.get_dict()


class Manager:
    def __init__(self):
        self.users = []

    def get_users(self):
        return self.users

    def get_json_object(self):
        res = []
        for user in self.users:
            user.update()
            user = {"name": user.name, "cookies": user.cookies}
            res.append(user)
        return res

    def add_user(self, username: str, cookies: map, session: requests.Session):
        user = User(username, cookies, session)
        self.users.append(user)
