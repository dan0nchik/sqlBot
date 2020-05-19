# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['sqlbot']
install_requires = \
['flask>=1.1,<2.0', 'google>=2.0,<3.0', 'telegram>=0.0.1,<0.0.2']

setup_kwargs = {
    'name': 'sqlbot',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Daniel Khromov',
    'author_email': 'danielkhromov@gmail.com',
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
