# -*- coding: utf-8 -*-
from os.path import join, dirname
from setuptools import setup, find_packages

VERSION = (0, 1, 0)
__version__ = VERSION
__versionstr__ = '.'.join(map(str, VERSION))

with open(join(dirname(__file__), 'README.rst')) as f:
    long_description = f.read().strip()

tests_require = [
    'pytest >= 3.3.0', 'tox', 'mock', 'coverage'
]

setup(
    name='pulsedive',
    description='Python client for Pulsedive API',
    license="MIT License",
    url='https://github.com/pberba/pulsedive-py',
    long_description=long_description,
    version=__versionstr__,
    author='Pepe Berba',
    author_email='jdpberba@gmail.com',
    packages=find_packages(
        where='.',
        exclude=('tests', )
    ),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    install_requires=['requests'],
    extras_require={
        'develop': tests_require + ["sphinx", "sphinx_rtd_theme"],
    }
)
