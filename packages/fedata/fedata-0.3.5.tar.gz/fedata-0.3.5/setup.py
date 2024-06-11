# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fedata',
 'fedata.exceptions',
 'fedata.hub',
 'fedata.load',
 'fedata.split',
 'fedata.transform',
 'fedata.utils']

package_data = \
{'': ['*']}

install_requires = \
['datasets>=2.8.0',
 'matplotlib>=3.7.1',
 'numpy>=1.24.1',
 'scikit-learn>=1.2.0',
 'torchaudio>=2.0.2',
 'torchvision>=0.15.1']

setup_kwargs = {
    'name': 'fedata',
    'version': '0.3.5',
    'description': '',
    'long_description': '',
    'author': 'Scolpe',
    'author_email': 'maciejzuziak101@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10.9,<4.0.0',
}


setup(**setup_kwargs)
