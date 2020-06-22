#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

requirements = []
setup_requirements = ['pytest-runner', ]
test_requirements = ['pytest', ]

data_files = [('api', ['service_registry/api/swagger.yaml'])]

setup(
    author="Jonathan Dursi",
    author_email='jonathan@dursi.ca',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    description="A model variant service demonstarting CanDIG API best practices and stack/tooling",
    install_requires=requirements,
    license="GNU General Public License v3",
    include_package_data=True,
    keywords='service_registry',
    name='service_registry',
    packages=find_packages(include=['service_registry']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    data_files=data_files,
    url='https://github.com/CanDIG/service_registry',
    version='0.1.1',
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'service_registry = service_registry.__main__:main'
            ]
        },
)
