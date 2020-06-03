# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


from setuptools import setup, find_packages
import moon_engine


setup(

    name='moon_engine',

    version=moon_engine.__version__,

    packages=find_packages(),

    author="Thomas Duval",

    author_email="thomas.duval@orange.com",

    description="",

    long_description=open('README.md').read(),

    install_requires=list(filter(
            lambda s: (len(s.strip()) > 0 and s.strip()[0] != '#'),
            open('requirements.txt').read().split('\n'))),

    include_package_data=True,

    url='',

    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 1 - Planning",
        "License :: OSI Approved",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],

    entry_points={
        'console_scripts': [
            'moon_engine = moon_engine.__main__:run',
        ],
    }
)
