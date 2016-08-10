#!/usr/bin/env python


# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.
from setuptools import setup, find_packages
from moonclient import __version__

PROJECT = 'python-moonclient'

# Change docs/sphinx/conf.py too!
VERSION = __version__

try:
    long_description = open('README.rst', 'rt').read()
except IOError:
    long_description = ''

setup(
    name=PROJECT,
    version=VERSION,

    description='Python Moon client',
    long_description=long_description,

    author='Thomas Duval',
    author_email='thomas.duval@orange.com',

    url='https://github.com/...',
    download_url='https://github.com/.../tarball/master',

    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: Apache Software License',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.2',
                 'Intended Audience :: Developers',
                 'Environment :: Console',
                 ],

    platforms=['Any'],

    scripts=[],

    provides=[],
    install_requires=['cliff'],

    namespace_packages=[],
    packages=find_packages(),
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'moon = moonclient.shell:main'
        ],
        'moon.client': [
            'template_list = moonclient.configuration:TemplatesList',
            'aggregation_algorithm_list = moonclient.configuration:AggregationAlgorithmsList',
            'submetarule_algorithm_list = moonclient.configuration:SubMetaRuleAlgorithmsList',

            'tenant_add = moonclient.tenants:TenantAdd',
            'tenant_set = moonclient.tenants:TenantSet',
            'tenant_list = moonclient.tenants:TenantList',
            'tenant_show = moonclient.tenants:TenantShow',
            'tenant_delete = moonclient.tenants:TenantDelete',

            'intraextension_select = moonclient.intraextension:IntraExtensionSelect',
            'intraextension_add = moonclient.intraextension:IntraExtensionCreate',
            'intraextension_list = moonclient.intraextension:IntraExtensionList',
            'intraextension_delete = moonclient.intraextension:IntraExtensionDelete',
            'intraextension_show = moonclient.intraextension:IntraExtensionShow',
            'intraextension_init = moonclient.intraextension:IntraExtensionInit',

            'subject_list = moonclient.subjects:SubjectsList',
            'subject_add = moonclient.subjects:SubjectsAdd',
            'subject_delete = moonclient.subjects:SubjectsDelete',
            'object_list = moonclient.objects:ObjectsList',
            'object_add = moonclient.objects:ObjectsAdd',
            'object_delete = moonclient.objects:ObjectsDelete',
            'action_list = moonclient.actions:ActionsList',
            'action_add = moonclient.actions:ActionsAdd',
            'action_delete = moonclient.actions:ActionsDelete',
            'subject_category_list = moonclient.subject_categories:SubjectCategoriesList',
            'subject_category_add = moonclient.subject_categories:SubjectCategoriesAdd',
            'subject_category_delete = moonclient.subject_categories:SubjectCategoriesDelete',
            'object_category_list = moonclient.object_categories:ObjectCategoriesList',
            'object_category_add = moonclient.object_categories:ObjectCategoriesAdd',
            'object_category_delete = moonclient.object_categories:ObjectCategoriesDelete',
            'action_category_list = moonclient.action_categories:ActionCategoriesList',
            'action_category_add = moonclient.action_categories:ActionCategoriesAdd',
            'action_category_delete = moonclient.action_categories:ActionCategoriesDelete',
            'subject_scope_list = moonclient.subject_scopes:SubjectScopesList',
            'subject_scope_add = moonclient.subject_scopes:SubjectScopesAdd',
            'subject_scope_delete = moonclient.subject_scopes:SubjectScopesDelete',
            'object_scope_list = moonclient.object_scopes:ObjectScopesList',
            'object_scope_add = moonclient.object_scopes:ObjectScopesAdd',
            'object_scope_delete = moonclient.object_scopes:ObjectScopesDelete',
            'action_scope_list = moonclient.action_scopes:ActionScopesList',
            'action_scope_add = moonclient.action_scopes:ActionScopesAdd',
            'action_scope_delete = moonclient.action_scopes:ActionScopesDelete',
            'subject_assignment_list = moonclient.subject_assignments:SubjectAssignmentsList',
            'subject_assignment_add = moonclient.subject_assignments:SubjectAssignmentsAdd',
            'subject_assignment_delete = moonclient.subject_assignments:SubjectAssignmentsDelete',
            'object_assignment_list = moonclient.object_assignments:ObjectAssignmentsList',
            'object_assignment_add = moonclient.object_assignments:ObjectAssignmentsAdd',
            'object_assignment_delete = moonclient.object_assignments:ObjectAssignmentsDelete',
            'action_assignment_list = moonclient.action_assignments:ActionAssignmentsList',
            'action_assignment_add = moonclient.action_assignments:ActionAssignmentsAdd',
            'action_assignment_delete = moonclient.action_assignments:ActionAssignmentsDelete',

            'aggregation_algorithm_show = moonclient.metarules:AggregationAlgorithmsList',
            'aggregation_algorithm_set = moonclient.metarules:AggregationAlgorithmSet',

            'submetarule_show = moonclient.metarules:SubMetaRuleShow',
            'submetarule_set = moonclient.metarules:SubMetaRuleSet',


            'rule_list = moonclient.rules:RulesList',
            'rule_add = moonclient.rules:RuleAdd',
            'rule_delete = moonclient.rules:RuleDelete',

            'log = moonclient.logs:LogsList',

            'test = moonclient.tests:TestsLaunch',
        ],
    },

    zip_safe=False,
)