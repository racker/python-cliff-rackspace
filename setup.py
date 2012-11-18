#!/usr/bin/env python
# Copyright 2012 Rackspace
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
import sys

from distutils.util import convert_path
from distutils.core import Command
from fnmatch import fnmatchcase
from setuptools import setup, find_packages
from subprocess import call


def read_version_string():
    version = None
    sys.path.insert(0, os.path.join(os.getcwd()))
    from cliff_rackspace import __version__
    version = __version__
    sys.path.pop(0)
    return version


setup(
    name='cliff-rackspace',
    version=read_version_string(),
    description='Rackspace Python cliff library extensions.',
    author='Rackspace Hosting',
    author_email='sr@rackspace.com',
    url='https://github.com/racker/python-cliff-rackspace',
    classifiers=['Development Status :: 4 - Beta',
                 'License :: OSI Approved :: Apache Software License',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2.6',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: Implementation :: PyPy',
                 'Environment :: Console',
                 ],
    platforms=['Any'],
    scripts=[],
    provides=[],
    install_requires=[],
    namespace_packages=[],
    packages=find_packages()
)
