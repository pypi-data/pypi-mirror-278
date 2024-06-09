# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clandestino_sqlite']

package_data = \
{'': ['*']}

install_requires = \
['clandestino-interfaces>=0.1.0,<0.2.0', 'python-decouple>=3.8,<4.0']

setup_kwargs = {
    'name': 'clandestino-sqlite',
    'version': '0.1.1',
    'description': 'Clandestino SQLite implementation',
    'long_description': '# Clandestino Sqlite\n\nMain project [here](https://github.com/CenturyBoys/clandestino)\n\nThis project uses native python [sqlite3](https://docs.python.org/3/library/sqlite3.html).\n',
    'author': 'XimitGaia',
    'author_email': 'im.ximit@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
