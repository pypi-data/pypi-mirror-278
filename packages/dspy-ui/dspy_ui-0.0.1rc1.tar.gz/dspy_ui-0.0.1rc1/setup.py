# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dspy_ui']

package_data = \
{'': ['*']}

install_requires = \
['dspy-ai==2.4.9']

setup_kwargs = {
    'name': 'dspy-ui',
    'version': '0.0.1rc1',
    'description': '',
    'long_description': '',
    'author': 'Tom Dörr',
    'author_email': 'tomdoerr96@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.3,<4.0',
}


setup(**setup_kwargs)
