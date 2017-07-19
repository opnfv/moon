# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

from setuptools import setup, find_packages
import moon_db


with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(

    name='moon_db',

    version=moon_db.__version__,

    packages=find_packages(),

    author="Thomas Duval",

    author_email="thomas.duval@orange.com",

    description="This library is a helper to interact with the Moon database.",

    long_description=open('README.rst').read(),

    install_requires=required,

    include_package_data=True,

    url='https://git.opnfv.org/cgit/moon/',

    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 1 - Planning",
        "License :: OSI Approved",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],

    entry_points={
        "moon_db.driver":
            [
                "sql = moon_db.backends.sql:SQLConnector",
                "flat = moon_db.backends.flat:LogConnector",
                "memory = moon_db.backends.memory:ConfigurationConnector",
            ],
        'console_scripts': [
            'moon_db_manager = moon_db.db_manager:run',
        ],
    }

)
