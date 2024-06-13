from Cryptodome.Random import get_random_bytes
from ..Utils import HexBytes

DEFAULT_SALT = HexBytes('0e25b3489775f493')

class Salt:

    @classmethod
    def create(cls):
        return cls(get_random_bytes(8))
    def __init__(self, keys: bytes = DEFAULT_SALT) -> None:
        self.__k__ = self.create() if not keys else keys
    def __str__(self) -> str:
        return str(self.__k__)
    def __repr__(self) -> str:
        return str(self.__k__)
    def __bytes__(self):
        return self.__k__    
