# Software Name: MOON

# Version: 5.4

# SPDX-FileCopyrightText: Copyright (c) 2018-2020 Orange and its contributors
# SPDX-License-Identifier: Apache-2.0

# This software is distributed under the 'Apache License 2.0',
# the text of which is available at 'http://www.apache.org/licenses/LICENSE-2.0.txt'
# or see the "LICENSE" file for more details.


import os
import shutil
from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop
import moon_manager


def initConfiguration():
    if os.name == "posix":
        try:
            os.mkdir("/etc/moon")
        except FileExistsError:
            pass
        if not os.path.exists(os.path.join("/etc", "moon", "moon.yaml")):
            print("Installing configuration file in /etc")
            shutil.copy(os.path.join("conf", "moon.yaml"),
                        os.path.join("/etc", "moon"))
        # else:
        #     raise NotImplementedError('You should install configuration file somewhere '
        #                                 'on your system')


class CustomInstallCommand(install):
    """Customized setuptools install command - install configuration file in etc."""
    
    def run(self):
        install.run(self)
        initConfiguration()


class CustomDevelopCommand(develop):
    """Customized setuptools develop command - install configuration file in etc."""
    
    def run(self):
        develop.run(self)
        initConfiguration()
        with open('requirements.txt') as f:
            requirements = filter(
                    lambda s: (len(s)>0 and s.strip()[0]!='#'),
                    f.read().split('\n'))
            print('requirements', requirements)


setup(

    name='moon_manager',

    version=moon_manager.__version__,

    packages=find_packages(),

    author="Thomas Duval",

    author_email="thomas.duval@orange.com",

    description="",

    long_description=open('README.md').read(),

    install_requires=list(filter(
            lambda s: (len(s) > 0 and s.strip()[0] != '#'),
            open('requirements.txt').read().split('\n'))),

    data_files=[
        ("moon", ["conf/moon.yaml"]),
        ("moon", ["moonrc"])
    ],


    include_package_data=True,

    cmdclass={
        'develop': CustomDevelopCommand,
        'install': CustomInstallCommand,
    },

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
            'moon_manager = moon_manager.__main__:run',
            'moon_manager_setup = moon_manager.manager_setup:setup'
        ],

    }

)
