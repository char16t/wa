try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': 'wa',
    'author': 'Valeriy Manenkov',
    'author_email': 'v.manenkov@gmail.com',
    'version': '0.1.0',
    'install_requires': [],
    'packages': ['wa'],
    'entry_points' : {
        'console_scripts': [
            'wa=wa.core:main'
        ]
    }
}

setup(**config)
