from typing import Union
from Cryptodome.Protocol.KDF import PBKDF2
from Cryptodome.Hash import SHA1

from .Salt import Salt

DEFAULT_PASSWORD = '3686494f576aa51fe5a8c3f92d8b1bd5'

class Password:

    @staticmethod
    def __check_password__(Password: Union[str, bytes]):
        if isinstance(Password, str):
            return Password.encode('utf-8')
        elif isinstance(Password, bytes):
            return Password
        else:
            raise TypeError('Password must be a string or bytes')

    @staticmethod
    def __check_salt__(salt: Union[Salt, bytes, str]):
        if isinstance(salt, Salt):
            return bytes(salt)
        elif isinstance(salt, bytes):
            return salt
        elif isinstance(salt, str):
            return salt.encode('utf-8')
        else:
            raise TypeError('Salt must be a string or bytes')
    
    @classmethod
    def create(cls, Password: Union[str, bytes], salt: Union[Salt, bytes, str], count: int = 1, dkLen: int = 16, hmac_hash_module = SHA1, addTextFront: str = '', addTextBack: str = ''):
        return cls(addTextFront + PBKDF2(cls.__check_password__(Password), cls.__check_salt__(salt), dkLen, count, hmac_hash_module=hmac_hash_module).hex() + addTextBack)
    def __init__(self, password: str = DEFAULT_PASSWORD) -> None:
        self.PBKDF2 = password
    def __str__(self) -> str:
        return self.PBKDF2
    def __repr__(self) -> str:
        return self.PBKDF2
    def __bytes__(self):
        return self.PBKDF2.encode('utf-8')
