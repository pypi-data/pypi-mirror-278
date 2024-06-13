# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['master_tuyul_sdk',
 'master_tuyul_sdk.Cipher',
 'master_tuyul_sdk.Database',
 'master_tuyul_sdk.Gmail',
 'master_tuyul_sdk.Provider',
 'master_tuyul_sdk.Provider.Connection',
 'master_tuyul_sdk.Provider._certificate',
 'master_tuyul_sdk.Utils']

package_data = \
{'': ['*']}

install_requires = \
['base58==2.1.1',
 'bs4>=0.0.2,<0.0.3',
 'chardet==5.2.0',
 'colorama==0.4.6',
 'google-api-python-client==2.131.0',
 'httpx[http2,socks]==0.27.0',
 'lxml==5.2.2',
 'pycryptodomex==3.20.0',
 'python-dotenv>=1.0.1,<2.0.0',
 'random-user-agent==1.0.1',
 'requests-toolbelt==0.10.1',
 'requests==2.31.0',
 'sqlalchemy-utils==0.41.2',
 'sqlalchemy==2.0.30',
 'urllib3==1.26.15']

setup_kwargs = {
    'name': 'master-tuyul-sdk',
    'version': '0.1.2',
    'description': '',
    'long_description': '',
    'author': 'DesKaOne',
    'author_email': 'DesKaOne@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
