# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['b_proxy']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=2.7.3,<3.0.0']

setup_kwargs = {
    'name': 'b-proxy',
    'version': '0.0.1rc1',
    'description': '',
    'long_description': '',
    'author': 'Antoni Oktha Fernandes',
    'author_email': '37358597+DesKaOne@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
