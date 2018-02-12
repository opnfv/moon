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
            'moon = python_moonclient.moon:main'
        ],
        'moon': [
          'pdp_list = python_moonclient.cli.pdps:Pdps',
          'pdp_create = python_moonclient.cli.pdps:CreatePdp',
          'pdp_delete = python_moonclient.cli.pdps:DeletePdp',
          'pdp_map = python_moonclient.cli.pdps:MapPdp',
          'policy_list = python_moonclient.cli.policies:Policies',
          'policy_delete = python_moonclient.cli.policies:DeletePolicy',
          'project_list = python_moonclient.cli.projects:Projects',
          'slave_list = python_moonclient.cli.slaves:Slaves',
          'slave_set = python_moonclient.cli.slaves:SetSlave',
          'slave_delete = python_moonclient.cli.slaves:DeleteSlave',
          'authz_send = python_moonclient.cli.authz:SendAuthz'
        ], 
      #      'moon_get_keystone_projects = python_moonclient.scripts:get_keystone_projects',
      #      'moon_get_pdp = python_moonclient.scripts:get_pdp',
      #      'moon_create_pdp = python_moonclient.scripts:create_pdp',
      #      'moon_delete_pdp = python_moonclient.scripts:delete_pdp',
      #      'moon_delete_policy = python_moonclient.scripts:delete_policy',
      #      'moon_map_pdp_to_project = python_moonclient.scripts:map_pdp_to_project',
      #      'moon_send_authz_to_wrapper = python_moonclient.scripts:send_authz_to_wrapper',
      #      'moon_get_slaves = python_moonclient.scripts:get_slaves',
      #      'moon_set_slave = python_moonclient.scripts:set_slave',
      #      'moon_delete_slave = python_moonclient.scripts:delete_slave'
      #  ],
    }

)
