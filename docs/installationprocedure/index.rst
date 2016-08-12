.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) ruan.he@orange.com & thomas.duval@orange.com

*****************************
OPNFV MOON installation guide
*****************************

.. toctree::
   :numbered:
   :maxdepth: 2


============
Introduction
============

The Moon platform is composed of 3 components :
* keystone-moon
* keystonemiddleware-moon
* python-moonclient

keystone-moon
=============
This component replaces the Keystone component of the OpenStack platform.
All basic functions of the original component were maintained but we add some new functions (specially authorization functions)

keystonemiddleware-moon
=======================
This component replaces the KeystoneMiddleware component of the OpenStack platform.
The main function added was to intercept all actions from Nova and Swift in order to retrieve an authorization token
from the Keystone-moon component.

python-moonclient
=================
The MoonClient is an interactive script to drive the Keystone-Moon component through the network.

=================
Packages creation
=================

Packages can be found on https://github.com/dthom/moon-bin

keystone-moon package
=====================

The Keystone-Moon can be package into 2 forms.
The first form is in traditional Python package :

.. code-block:: bash

    cd moon_repo/keystone-moon
    python setup.py sdist
    ls dist

We develop a script to build a Debian package, this script is located in `moon_repo/debian/keystone-moon`

.. code-block:: bash

    cd moon_repo/debian/keystone-moon
    python create_deb.py


keystonemiddleware-moon package
===============================

The KeystoneMiddleware-Moon can be package into 2 forms.
The first form is in traditional Python package :

.. code-block:: bash

    cd moon_repo/keystonemiddleware-moon
    python setup.py sdist
    ls dist

We develop a script to build a Debian package, this script is located in `moon_repo/debian/keystonemiddleware-moon`

.. code-block:: bash

    cd moon_repo/debian/keystonemiddleware-moon
    python create_deb.py


python-moonclient package
=========================

There is only one type of package for the Moon client:

.. code-block:: bash

    cd moon_repo/moonclient
    python setup.py sdist
    ls dist


============
Installation
============

This installation procedure only describe the installation of a standalone Moon platform.


Pre-requisite
=============

To install the Moon platform, you will need a working Linux server box.
The platform is tested on an up-to-date Ubuntu 16.04 box.

You can build your own packages or you can download stable ones on https://github.com/dthom/moon-bin

Installation
============

First of all, you must install dependencies for the Keystone-moon package, then you can download pre-built packages or
create them by yourself. Endly, you can install Keystone-Moon and MoonClient packages:

.. code-block:: bash

    cd /tmp
    wget https://github.com/dthom/moon-bin/archive/master.zip
    unzip master.zip
    PKGS = $(python3 /tmp/moon-bin-master/tools/get_deb_depends.py /tmp/moon-bin-master/*.deb)
    sudo apt-get install $PKGS
    sudo dpkg -i /tmp/moon-bin-master/keystone_latest-moon_all.deb
    sudo pip install --upgrade /tmp/moon-bin-master/python-moonclient-latest.tar.gz

At this point, the Nova and Swift components must be installed on the same box or on an other box.
See http://docs.openstack.org/ for more explanation.

Nova and Swift components automatically installed the python-keystonemiddleware package.
We have to replace it with the dedicated Moon one:

.. code-block:: bash

    cd /tmp
    sudo dpkg -i /tmp/moon-bin-master/python3-keystonemiddleware_latest-moon_all.deb
    sudo dpkg -i /tmp/moon-bin-master/python-keystonemiddleware_latest-moon_all.deb

Note: if you installed Nova and Swift in 2 different nodes, you must install python-keystonemiddleware
in those 2 nodes.

Configuration
=============

For Keystone, the following files must be configured, some modifications may be needed, specially passwords:

/etc/keystone/keystone-paste.ini

.. code-block:: bash

    sudo cp /etc/keystone/keystone-paste.ini /etc/keystone/keystone-paste.ini.bak
    sudo sed "3i[pipeline:moon_pipeline]\npipeline = sizelimit url_normalize request_id build_auth_context token_auth admin_token_auth json_body ec2_extension_v3 s3_extension moon_service\n\n[app:moon_service]\nuse = egg:keystone#moon_service\n" /etc/keystone/keystone-paste.ini > /tmp/keystone-paste.ini
    sudo cp /tmp/keystone-paste.ini /etc/keystone/keystone-paste.ini
    sudo sed "s/use = egg:Paste#urlmap/use = egg:Paste#urlmap\n\/moon = moon_pipeline/" /etc/keystone/keystone-paste.ini > /tmp/keystone-paste.ini
    sudo cp /tmp/keystone-paste.ini /etc/keystone/keystone-paste.ini

/etc/keystone/keystone.conf

.. code-block:: bash

    cat << EOF | sudo tee -a /etc/keystone/keystone.conf
    [moon]

    # Configuration backend driver
    configuration_driver = keystone.contrib.moon.backends.memory.ConfigurationConnector

    # Tenant backend driver
    tenant_driver = keystone.contrib.moon.backends.sql.TenantConnector

    # Authorisation backend driver
    authz_driver = keystone.contrib.moon.backends.flat.SuperExtensionConnector

    # IntraExtension backend driver
    intraextension_driver = keystone.contrib.moon.backends.sql.IntraExtensionConnector

    # InterExtension backend driver
    interextension_driver = keystone.contrib.moon.backends.sql.InterExtensionConnector

    # Logs backend driver
    log_driver = keystone.contrib.moon.backends.flat.LogConnector

    # Local directory where all policies are stored
    policy_directory = /etc/keystone/policies

    # Local directory where Root IntraExtension configuration is stored
    root_policy_directory = policy_root

    # URL of the Moon master
    master = 'http://localhost:35357/'

    # Login of the Moon master
    master_login = 'admin'

    # Password of the Moon master
    master_password = 'nomoresecrete'
    EOF


The logging system must be configured :

.. code-block:: bash

    sudo mkdir /var/log/moon/
    sudo chown keystone /var/log/moon/

    sudo addgroup moonlog

    sudo chgrp moonlog /var/log/moon/

    sudo touch /var/log/moon/keystonemiddleware.log
    sudo touch /var/log/moon/system.log

    sudo chgrp moonlog /var/log/moon/keystonemiddleware.log
    sudo chgrp moonlog /var/log/moon/system.log
    sudo chmod g+rw /var/log/moon
    sudo chmod g+rw /var/log/moon/keystonemiddleware.log
    sudo chmod g+rw /var/log/moon/system.log

    sudo adduser keystone moonlog
    sudo adduser swift moonlog
    sudo adduser nova moonlog

The Keystone database must be updated:

.. code-block:: bash

    sudo /usr/bin/keystone-manage db_sync
    sudo /usr/bin/keystone-manage db_sync --extension moon

And, Apache must be restarted:

.. code-block:: bash

    sudo systemctl restart apache.service

In order to Nova to be able to communicate with Keystone-Moon, you must update the Nova KeystoneMiddleware configuration file.
To achieve this, a new filter must be added in `/etc/nova/api-paste.ini` and this filter must be added to the composite data.
The filter is:

.. code-block:: bash

    [filter:moon]
    paste.filter_factory = keystonemiddleware.moon_agent:filter_factory
    authz_login=admin
    authz_password=password
    logfile=/var/log/moon/keystonemiddleware.log

Here is some bash lines to insert this into the Nova configuration file:

.. code-block:: bash

    sudo cp /etc/nova/api-paste.ini /etc/nova/api-paste.ini.bak2
    sudo sed "/^keystone = / s/keystonecontext/keystonecontext moon/" /etc/nova/api-paste.ini > /tmp/api-paste.ini
    sudo cp /tmp/api-paste.ini /etc/nova/api-paste.ini

    echo -e "\n[filter:moon]\npaste.filter_factory = keystonemiddleware.moon_agent:filter_factory\nauthz_login=admin\nauthz_password=password\nlogfile=/var/log/moon/keystonemiddleware.log\n" | sudo tee -a /etc/nova/api-paste.ini

Nova can then be restarted:

.. code-block:: bash

    for service in nova-compute nova-api nova-cert nova-conductor nova-consoleauth nova-scheduler ; do
        sudo service ${service} restart
    done

In order to Swift to be able to communicate with Keystone-Moon, you must update the Swift KeystoneMiddleware configuration file.
To achieve this, a new filter must be added in `/etc/swift/proxy-server.conf` and this filter must be added to the composite data.
The filter is (exactly the same as Nova):

.. code-block:: bash

    [filter:moon]
    paste.filter_factory = keystonemiddleware.moon_agent:filter_factory
    authz_login=admin
    authz_password=password
    logfile=/var/log/moon/keystonemiddleware.log

Here is some bash lines to insert this into the Nova configuration file:

.. code-block:: bash

    sudo cp /etc/swift/proxy-server.conf /etc/swift/proxy-server.conf.bak2
    sudo sed "/^pipeline = / s/proxy-server/moon proxy-server/" /etc/swift/proxy-server.conf > /tmp/proxy-server.conf
    sudo cp /tmp/proxy-server.conf /etc/swift/proxy-server.conf

    echo -e "\n[filter:moon]\npaste.filter_factory = keystonemiddleware.moon_agent:filter_factory\nauthz_login=admin\nauthz_password=password\nlogfile=/var/log/moon/keystonemiddleware.log\n" | sudo tee -a /etc/swift/proxy-server.conf

Swift can then be restarted:

.. code-block:: bash

    for service in swift-account swift-account-replicator \
                    swift-container-replicator  swift-object swift-object-updater \
                    swift-account-auditor swift-container swift-container-sync \
                    swift-object-auditor swift-proxy swift-account-reaper swift-container-auditor \
                    swift-container-updater swift-object-replicator ; do
        sudo service ${service} status
    done



Running tests
=============

After a successful installation of the Moon platform, you can execute some tests to see if the platform is
up and running. Be patient, the latest test takes time (5 to 20 minutes).

.. code-block:: bash

    export OS_USERNAME=admin
    export OS_PASSWORD=password
    export OS_REGION_NAME=What_ever_you_want
    export OS_TENANT_NAME=admin
    export OS_AUTH_URL=http://localhost:5000/v2.0

    # See if Nova is up and running:
    nova list

    # See if Swift is up and running:
    swift stat

    # See if Keystone-Moon is up and running
    moon intraextension list
    # you must  see one extension (named root)
    moon test --self


Revision: _sha1_

Build date: |today|