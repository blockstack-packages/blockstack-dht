#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Blockstack
    ~~~~~
    copyright: (c) 2014-2015 by Halfmoon Labs, Inc.
    copyright: (c) 2016 by Blockstack.org

    This file is part of Blockstack

    Blockstack is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Blockstack is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with Blockstack. If not, see <http://www.gnu.org/licenses/>.
"""

from setuptools import setup, find_packages

exec(open("blockstack_dht/version.py").read())

setup(
    name='blockstack-server',
    version=__version__,
    url='https://github.com/blockstack/blockstack-dht',
    license='GPLv3',
    author='Blockstack.org',
    author_email='support@blockstack.org',
    description='DHT service for Blockstack zonefiles',
    keywords='blockchain bitcoin btc cryptocurrency name key value store data dht',
    packages=find_packages(),
    scripts=['bin/blockstack-dht'],
    download_url='https://github.com/blockstack/blockstack-dht/archive/master.zip',
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'kademlia==0.5',
        'Twisted==15.5.0',
        'zope.interface==4.1.3'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet',
        'Topic :: Security :: Cryptography',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
