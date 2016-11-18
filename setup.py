#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='sqldoc',
    version='0.1.0',
    description="Tool from generating database HTML documentation.",
    long_description=readme + '\n\n' + history,
    author="Ivan Korhner",
    author_email='korhner@gmail.com',
    url='https://github.com/korhner/sqldoc',
    packages=[
        'sqldoc',
    ],
    package_dir={'sqldoc':
                 'sqldoc'},
    entry_points={
        'console_scripts': [
            'sqldoc=sqldoc.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='sqldoc',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)