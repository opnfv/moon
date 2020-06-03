# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


from setuptools import setup, find_packages
import moon_utilities

with open('requirements.txt') as f:
    required = list(filter(
            lambda s: (len(s.strip()) > 0 and s.strip()[0] != '#'),
            f.read().split('\n')))

setup(

    name='moon_utilities',

    version=moon_utilities.__version__,

    packages=find_packages(),

    author='Thomas Duval',

    author_email='thomas.duval@orange.com',

    description='Some utilities for all the Moon components',

    long_description=open('README.md').read(),

    install_requires=required,

    include_package_data=True,

    url='',

    classifiers=[
        'Programming Language :: Python :: 3',
        'Development Status :: 1 - Planning',
        'License :: OSI Approved',
        'Natural Language :: English',
        'Operating System :: OS Independent',
    ],

    entry_points={
        'console_scripts': [
            'generate_opst_policy = moon_utilities.generate_opst_policy:main',
        ],

    }

)
