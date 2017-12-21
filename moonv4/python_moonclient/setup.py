# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

from setuptools import setup, find_packages
import moonclient

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(

    name='python-moonclient',

    version=moonclient.__version__,

    packages=find_packages(),

    author='Thomas Duval & Ruan He',

    author_email='thomas.duval@orange.com, ruan.he@orange.com',

    description='client lib for all the Moon components',

    long_description=open('README.md').read(),

    install_requires=required,

    include_package_data=True,

    url='https://git.opnfv.org/cgit/moon',

    classifiers=[
        'Programming Language :: Python :: 3',
        'Development Status :: 1 - Planning',
        'License :: OSI Approved',
        'Natural Language :: English',
        'Operating System :: OS Independent',
    ],

)
