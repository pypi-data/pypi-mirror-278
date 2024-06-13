from enum import Enum, auto
import ssl

from typing import Any, Iterable, Optional
import importlib.resources as pkg_resources

from requests.adapters import HTTPAdapter as __adapter__
from urllib3.poolmanager import PoolManager  # type: ignore

from . import _certificate
from urllib3 import Retry as __retry__

DEFAULT_CIPHERS = ":".join(
    [
        "ECDHE+AESGCM",
        "ECDHE+CHACHA20",
        "DHE+AESGCM",
        "DHE+CHACHA20",
        "ECDH+AESGCM",
        "DH+AESGCM",
        "ECDH+AES",
        "DH+AES",
        "RSA+AESGCM",
        "RSA+AES",
        "!aNULL",
        "!eNULL",
        "!MD5",
        "!DSS",
    ]
)

MY_CHIPER = ':'.join(
    [
        "TLS_AES_256_GCM_SHA384",
        "TLS_CHACHA20_POLY1305_SHA256",
        "TLS_AES_128_GCM_SHA256",
        "ECDHE-ECDSA-AES256-GCM-SHA384",
        "ECDHE-RSA-AES256-GCM-SHA384",
        "ECDHE-ECDSA-AES128-GCM-SHA256",
        "ECDHE-RSA-AES128-GCM-SHA256",
        "ECDHE-ECDSA-CHACHA20-POLY1305",
        "ECDHE-RSA-CHACHA20-POLY1305",
        "DHE-RSA-AES256-GCM-SHA384",
        "DHE-RSA-AES128-GCM-SHA256",
        "DHE-RSA-CHACHA20-POLY1305",
        "ECDHE-ECDSA-AES256-CCM8",
        "ECDHE-ECDSA-AES256-CCM",
        "ECDHE-ECDSA-AES128-CCM8",
        "ECDHE-ECDSA-AES128-CCM",
        "ECDHE-ECDSA-AES256-SHA384",
        "ECDHE-RSA-AES256-SHA384",
        "ECDHE-ECDSA-AES128-SHA256",
        "ECDHE-RSA-AES128-SHA256",
        "ECDHE-ECDSA-AES256-SHA",
        "ECDHE-RSA-AES256-SHA",
        "ECDHE-ECDSA-AES128-SHA",
        "ECDHE-RSA-AES128-SHA",
        "DHE-RSA-AES256-CCM8",
        "DHE-RSA-AES256-CCM",
        "DHE-RSA-AES128-CCM8",
        "DHE-RSA-AES128-CCM",
        "DHE-RSA-AES256-SHA256",
        "DHE-RSA-AES128-SHA256",
        "DHE-RSA-AES256-SHA",
        "DHE-RSA-AES128-SHA",
        "AES256-GCM-SHA384",
        "AES128-GCM-SHA256",
        "AES256-CCM8",
        "AES256-CCM",
        "AES128-CCM8",
        "AES128-CCM",
        "AES256-SHA256",
        "AES128-SHA256",
        "AES256-SHA",
        "AES128-SHA",
        'RC4-SHA'
    ]
)

class SSLContext(ssl.SSLContext):
    """SSLContext wrapper."""

    def set_alpn_protocols(self, alpn_protocols: Iterable[str]) -> None:
        """
        ALPN headers cause Google to return 403 Bad Authentication.
        """

def certificate():
    with pkg_resources.path(_certificate, 'cacert.pem') as p:
        return str(p)

class HTTPAdapter(__adapter__):
    
    def __init__(self, timeout=None, *args, **kwargs):
        self.timeout = timeout
        if "timeout" in kwargs:
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)
    
    """TLS tweaks."""

    def init_poolmanager(self, *args: Any, **kwargs: Any) -> None:
        """
        Secure settings from ssl.create_default_context(), but without
        ssl.OP_NO_TICKET which causes Google to return 403 Bad
        Authentication.
        """
        context = SSLContext()
        context.set_ciphers(MY_CHIPER)
        #context.set_alpn_protocols(ssl.PROTOCOL_SSLv23)
        context.verify_mode = ssl.CERT_REQUIRED
        context.options &= ~ssl.OP_NO_TICKET  # pylint: disable=E1101
        self.poolmanager = PoolManager(*args, ssl_context=context, **kwargs)

class ProxyType(Enum):
    
    socks5  = auto()
    http    = auto()

class ProxyParams:

    URL: str = None

    def __new__(cls, type: ProxyType, IP: str, PORT: int, USERNAME: Optional[str] = None, PASSWORD: Optional[str] = None) -> 'ProxyParams':
        if USERNAME is not None and PASSWORD is not None:
            build = f'{USERNAME}:{PASSWORD}@{IP}:{PORT}'
        else:
            build = f'{IP}:{PORT}'
        if type == ProxyType.http:
            setattr(ProxyParams, 'URL', f'http://{build}')
        elif type == ProxyType.socks5:
            setattr(ProxyParams, 'URL', f'socks5://{build}')
        return cls
