#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    'tox',
    'ddt',
]

setup(
    name='flake8_tuple',
    version='0.1.0',
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
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    entry_points={
        'flake8.extension': [
            'T80 = flake8_tuple:TupleChecker',
        ],
    }
)
