try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

__version__ = None

with open(local_file("wa/version.py")) as o:
    exec(o.read())

assert __version__ is not None

with open('README.rst') as f:
    long_description = f.read()

config = {
    'name': 'wa',
    'author': 'Valeriy Manenkov',
    'author_email': 'v.manenkov@gmail.com',
    'description': 'Workflow automation tool',
    'long_description': long_description,
    'license': 'MIT',
    'version': __version__,
    'url': 'https://github.com/char16t/wa',
    'download_url': 'https://github.com/char16t/wa/archive/master.tar.gz',
    'install_requires': ['pyyaml', 'Jinja2'],
    'packages': ['wa'],
    'entry_points': {
        'console_scripts': [
            'wa=wa.cli:main'
        ]
    },
    'classifiers': [
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
}

setup(**config)
