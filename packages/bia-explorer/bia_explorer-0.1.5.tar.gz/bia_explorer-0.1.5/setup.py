# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bia_explorer']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.3.0,<10.0.0',
 'aiobotocore>=2.0.0,<3.0.0',
 'bia-integrator-api>=0.3.0,<0.4.0',
 'dask>=2024.4.1,<2025.0.0',
 'jupyter>=1.0.0,<2.0.0',
 'ome-zarr>=0.8.3,<0.9.0',
 'pydantic>=1.10.2,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'zarr>=2.17.2,<3.0.0']

setup_kwargs = {
    'name': 'bia-explorer',
    'version': '0.1.5',
    'description': '',
    'long_description': 'None',
    'author': 'Matthew Hartley',
    'author_email': 'matthewh@ebi.ac.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
