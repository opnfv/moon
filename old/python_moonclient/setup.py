# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

from setuptools import setup, find_packages
import python_moonclient
import python_moonclient.core

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
          'authz_send = python_moonclient.cli.authz:SendAuthz',
          'import = python_moonclient.cli.import:Import',
          'export = python_moonclient.cli.export:Export',
          'model_list = python_moonclient.cli.models:Models',
          'subject_data_list = python_moonclient.cli.policies:SubjectDatas',
          'object_data_list = python_moonclient.cli.policies:ObjectDatas',
          'action_data_list = python_moonclient.cli.policies:ActionDatas',
          'subject_category_list = python_moonclient.cli.models:SubjectCategories',
          'object_category_list = python_moonclient.cli.models:ObjectCategories',
          'action_category_list = python_moonclient.cli.models:ActionCategories',
          'subject_category_create = python_moonclient.cli.models:SubjectCategoryAdd',
          'subject_data_create = python_moonclient.cli.policies:CreateSubjectData',
          'metarule_list = python_moonclient.cli.policies:MetaRules'
        ], 
    }

)
