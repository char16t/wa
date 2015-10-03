try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': 'wa',
    'author': 'Valeriy Manenkov',
    'author_email': 'v.manenkov@gmail.com',
    'description': 'Workflow automation tool',
    'license': 'MIT',
    'version': '0.1.0',
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
