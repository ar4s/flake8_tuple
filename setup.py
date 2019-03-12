#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def read(filename):
    with open(filename) as f:
        return f.read()


def find_version():
    version_file = read('flake8_tuple.py')
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M
    )
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


readme = read('README.rst')
history = read('HISTORY.rst').replace('.. :changelog:', '')

requirements = [
    'six',
    'flake8'
]

test_requirements = [
    'tox',
    'ddt',
]

setup(
    name='flake8_tuple',
    version=find_version(),
    description="Check code for 1 element tuple.",
    long_description=readme + '\n\n' + history,
    author="Arkadiusz Adamski",
    author_email='arkadiusz.adamski@gmail.com',
    url='https://github.com/ar4s/flake8_tuple',
    py_modules=[
        'flake8_tuple',
    ],
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='flake8_tuple',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='tests',
    tests_require=requirements + test_requirements,
    entry_points={
        'flake8.extension': [
            'T80 = flake8_tuple:TupleChecker',
        ],
    }
)
