# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

from setuptools import setup, find_packages
import python_moonclient

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(

    name='python-moonclient',

    version=python_moonclient.__version__,

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

    entry_points={
        'console_scripts': [
            'moon_get_keystone_projects = python_moonclient.scripts:get_keystone_projects',
            'moon_create_pdp = python_moonclient.scripts:create_pdp',
            'moon_get_pdp = python_moonclient.scripts:get_pdp',
            'moon_send_authz_to_wrapper = python_moonclient.scripts:send_authz_to_wrapper',
            'moon_delete_pdp = python_moonclient.scripts:delete_pdp',
            'moon_delete_policy = python_moonclient.scripts:delete_policy',
            'moon_map_pdp_to_project = python_moonclient.scripts:map_pdp_to_project'
        ],
    }

)
