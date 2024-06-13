# Copyright 2014 xjmz, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file
# except in compliance with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the
# License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.

"""
The setup script to install FOS SDK for python
"""
from __future__ import absolute_import
import io
import os
import re
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with io.open(os.path.join("flymeyun_fos", "__init__.py"), "rt") as f:
    SDK_VERSION = re.search(r"SDK_VERSION = b'(.*?)'", f.read()).group(1)


setup(
    name='flymeyun_fos',
    version=str(SDK_VERSION),
    install_requires=['pycryptodome>=3.8.0',
                      'future>=0.6.0',
                      'six>=1.4.0'],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, <4',
    packages=['flymeyun_fos',
              'flymeyun_fos.auth',
              'flymeyun_fos.http',
              'flymeyun_fos.retry',
              'flymeyun_fos.services',
              'flymeyun_fos.services.fos'],
    url='https://www.flymeyun.com/#/product/fos/index',
    license='Apache License 2.0',
    author='',
    author_email='',
    description='Flymeyun FOS SDK for python'
)
