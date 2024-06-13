from typing import Dict, Optional
from requests import Session

from .__utils__ import HTTPAdapter, ProxyParams
from ..Utils import version
from .Connection import AuthHTTPAdapter

class Requests:

    class new:

        def __new__(cls, BASE_URL: str, extra_headers: Dict[str, str] = dict(), proxyParams: Optional[ProxyParams] = None):
            if not proxyParams: proxy_url = None
            else: proxy_url = proxyParams.URL
            requests = Session()
            requests.mount(BASE_URL, AuthHTTPAdapter())        
            if not proxy_url: requests.proxies = dict()
            else: requests.proxies = dict(http = proxy_url, https = proxy_url)

            header: Dict[str, str] = dict()
            try:
                for k, v in zip(extra_headers.keys(), extra_headers.values()): header.update(**{k.lower():v})
                if not header.get('User-Agent'.lower()):
                    header.update(**{'User-Agent'.lower() : 'Tuyul-Online/{}'.format(version)})
            except AttributeError:
                if not header.get('User-Agent'.lower()):
                    header.update(**{'User-Agent'.lower() : 'Tuyul-Online/{}'.format(version)})
            
            requests.headers.update(**header)
            return requests

    def __new__(cls, timeout: int = 60, extra_headers: Dict[str, str] = dict(), proxyParams: Optional[ProxyParams] = None, Adapter: bool = False) -> 'Session':
        if not proxyParams: proxy_url = None
        else: proxy_url = proxyParams.URL
        requests = Session()
        if Adapter:
            adapter = HTTPAdapter(timeout=timeout)
            for scheme in ('http://', 'https://'): requests.mount(scheme, adapter)        
        if not proxy_url: requests.proxies = dict()
        else: requests.proxies = dict(http = proxy_url, https = proxy_url)

        header: Dict[str, str] = dict()
        try:
            for k, v in zip(extra_headers.keys(), extra_headers.values()): header.update(**{k.lower():v})
            if not header.get('User-Agent'.lower()):
                header.update(**{'User-Agent'.lower() : 'Tuyul-Online/{}'.format(version)})
        except AttributeError:
            if not header.get('User-Agent'.lower()):
                header.update(**{'User-Agent'.lower() : 'Tuyul-Online/{}'.format(version)})
        
        requests.headers.update(**header)
        return requests