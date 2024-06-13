import base64
from enum import Enum
from typing import Dict, Literal, Union
from Cryptodome.Hash import MD5
from Cryptodome.Cipher import AES as aes
import base58

from .Password import Password
from .Salt import Salt
from ..Utils import HexBytes

SIZE = aes.block_size

class Mode(Enum):
    MODE_ECB = aes.MODE_ECB
    MODE_CBC = aes.MODE_CBC
    MODE_CFB = aes.MODE_CFB
    MODE_OFB = aes.MODE_OFB
    MODE_CTR = aes.MODE_CTR
    MODE_OPENPGP = aes.MODE_OPENPGP
    MODE_CCM = aes.MODE_CCM
    MODE_EAX = aes.MODE_EAX
    MODE_SIV = aes.MODE_SIV
    MODE_GCM = aes.MODE_GCM
    MODE_OCB = aes.MODE_OCB

def to_bytes(data: Union[Password, str, bytes, Salt]):
    if isinstance(data, Password):
        return bytes(data)
    elif isinstance(data, Salt):
        return bytes(data)
    elif isinstance(data, str):
        return data.encode('utf-8')
    elif isinstance(data, bytes):
            return data
    else:
        raise TypeError('Password must be a string or bytes') 

def to_decode(PlainText: Union[str, bytes]):
    if isinstance(PlainText, str):
        try:
            decode = HexBytes(PlainText)
            if PlainText == decode.hex() and decode[:8] == b'Salted__':
                return decode
        except: pass
        try:
            decode = base64.b64decode(PlainText)
            if PlainText == base64.b64encode(decode).decode() and decode[:8] == b'Salted__':
                return decode
        except: pass
        try:
            decode = base58.b58decode(PlainText)
            if PlainText == base58.b58encode(decode).decode() and decode[:8] == b'Salted__':
                return decode
        except: pass
    elif isinstance(PlainText, (bytes, HexBytes, bytearray)):
        return PlainText
    else:
        raise TypeError('Data must be a string or bytes')

def pad(PlainText: bytes):
    return PlainText + (SIZE - len(PlainText) % SIZE) * bytes(chr(0), encoding='utf-8')
        
def unpad(PlainText: bytes):
    return ''.join([chr(s) if int(s) != 0 else '' for s in PlainText]).encode()

def create_key_iv( salt: Union[Salt, bytes, str], Password: Union[Password, bytes, str]):
    class Response:
        def __init__(self, key, iv) -> None:
            self.KEY: bytes = key
            self.IV: bytes  = iv
        def __repr__(self) -> str:
            return str(self.__dict__)
        def __str__(self) -> str:
            return str(self.__dict__)
        def json(self):
            return self.__dict__
    derived = b""
    while len(derived) < 48:
        hasher = MD5.new()
        hasher.update(derived[-16:] + to_bytes(Password) + to_bytes(salt))
        derived += hasher.digest()
    KEY = derived[0:32]
    IV  = derived[32:48]
    return Response(KEY, IV)

def encrypt(PlainText: Union[str, bytes], KEY: Union[str, bytes], IV: Union[str, bytes] = None, Salt: Union[str, bytes, Salt] = None, MODE: Mode = Mode.MODE_CBC):
    class Encrypt:
        def __init__(self, Result: Dict[str, any]) -> None:
            self.Bytes: bytes   = Result.get('Encrypt').get('Bytes')
            self.Base64: str    = Result.get('Encrypt').get('Base64')
            self.Base58: str    = Result.get('Encrypt').get('Base58')
            self.Hex: str       = Result.get('Encrypt').get('Hex')
            self.IV: str        = Result.get('IV')
            self.KEY: str       = Result.get('KEY')
            self.Salt: Union[str, None]= Result.get('Salt')
        def __str__(self) -> str:
            return str(self.__dict__)
        def __repr__(self) -> str:
            return str(self.__dict__)
        def json(self):
            self.__dict__
    cipher = HexBytes(aes.new(to_bytes(KEY), MODE.value, to_bytes(IV)).encrypt(pad(to_bytes(PlainText))))
    if Salt is not None:
        Salt    = to_bytes(Salt)
        Bytes   = HexBytes(b'Salted__' + Salt + cipher)
    else:
        Bytes   = cipher

    return Encrypt(dict(
        Encrypt = dict(
            Bytes   = Bytes,
            Base64  = base64.b64encode(Bytes).decode('utf-8'),
            Base58  = base58.b58encode(Bytes).decode('utf-8'),
            Hex     = Bytes.hex()
        ),
        IV      = to_bytes(IV).hex(),
        KEY     = to_bytes(KEY).hex(),
        Salt    = Salt.hex() if Salt is not None else None
    ))

def decrypt(PlainText: Union[str, bytes], KEY: Union[str, bytes], IV: Union[str, bytes], MODE: Mode = Mode.MODE_CBC):
    class Decrypt:
        def __init__(self, Result: Dict[str, any]) -> None:
            self.bytes: bytes   = Result.get('Decrypt').get('CipherBytes')
            self.string: str    = Result.get('Decrypt').get('CipherString')
            self.IV: str        = Result.get('IV')
            self.KEY: str       = Result.get('KEY')
        def __str__(self) -> str:
            return str(self.__dict__)
        def __repr__(self) -> str:
            return str(self.__dict__)
        def json(self):
            self.__dict__
    cipher = HexBytes(unpad(aes.new(to_bytes(KEY), MODE.value, to_bytes(IV)).decrypt(PlainText)))
    return Decrypt(dict(
        Decrypt = dict(
            CipherBytes     = cipher,
            CipherString    = cipher.decode(encoding='ascii')
        ),
        IV      = IV.hex(),
        KEY     = KEY.hex()
    ))

class Cipher:

    class encrypt:

        @staticmethod
        def create_encrypt_with_password(PlainText: Union[str, bytes], password: Union[str, bytes]):
            salt    = Salt.create()
            create  = create_key_iv(salt, Password.create(password, salt))
            return encrypt(PlainText, create.KEY, create.IV, salt)

        @staticmethod
        def create_encrypt_with_key_iv(PlainText: Union[str, bytes], KEY: Union[str, bytes], IV: Union[str, bytes]):
            return encrypt(PlainText, KEY, IV)

    class decrypt:
        
        @staticmethod
        def create_decrypt_with_password(PlainText: Union[str, bytes], password: Union[str, bytes]):
            decode  = to_decode(PlainText)
            create  = create_key_iv(decode[8:16], Password.create(password, decode[8:16]))
            return decrypt(decode[16:], create.KEY, create.IV)
        
        @staticmethod
        def create_decrypt_with_key_iv(PlainText: Union[str, bytes], KEY: Union[str, bytes], IV: Union[str, bytes]):
            return decrypt(PlainText, KEY, IV)