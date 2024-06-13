from .__utils__ import requests, AuthHTTPAdapter

class _Base:

    def __new__(cls, AUTH_URL: str):
        cls.__ses__ = requests.session()
        cls.__ses__.mount(AUTH_URL, AuthHTTPAdapter())
        return cls.__ses__