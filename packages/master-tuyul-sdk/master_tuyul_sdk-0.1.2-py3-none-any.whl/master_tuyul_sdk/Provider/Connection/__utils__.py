"""A python client library for Google Play Services OAuth."""
from __future__ import annotations

from collections.abc import MutableMapping
from importlib.metadata import version
import ssl
from typing import Any, Iterable

import requests

# Type annotations for urllib3 will be released with v2.
from urllib3.poolmanager import PoolManager  # type: ignore[import]

SSL_DEFAULT_CIPHERS = None
if version("urllib3") < "2.0.0a1":
    from urllib3.util.ssl_ import DEFAULT_CIPHERS  # type: ignore[import]

    SSL_DEFAULT_CIPHERS = DEFAULT_CIPHERS


class SSLContext(ssl.SSLContext):
    """SSLContext wrapper."""

    def set_alpn_protocols(self, alpn_protocols: Iterable[str]) -> None:
        """
        ALPN headers cause Google to return 403 Bad Authentication.
        """

class AuthHTTPAdapter(requests.adapters.HTTPAdapter):
    """TLS tweaks."""

    def init_poolmanager(self, *args: Any, **kwargs: Any) -> None:
        """
        Secure settings from ssl.create_default_context(), but without
        ssl.OP_NO_TICKET which causes Google to return 403 Bad
        Authentication.
        """
        context = SSLContext()
        if SSL_DEFAULT_CIPHERS:
            context.set_ciphers(SSL_DEFAULT_CIPHERS)
        context.verify_mode = ssl.CERT_REQUIRED
        context.options &= ~ssl.OP_NO_TICKET  # pylint: disable=E1101
        self.poolmanager = PoolManager(*args, ssl_context=context, **kwargs)
