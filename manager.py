import requests


class Manager:
    def __init__(self):
        self.__sessions = []

    def get_sessions(self):
        return self.__sessions

    def add_session(self, session: requests.Session):
        self.__sessions.append(session)
