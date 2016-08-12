.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) ruan.he@orange.com & thomas.duval@orange.com

******************************
OPNFV MOON configuration guide
******************************

.. toctree::
   :numbered:
   :maxdepth: 2


============
Introduction
============

Moon must be configured through the standard Keystone configuration files and the standard KeystoneMiddleware configuration files:
* /etc/keystone/keystone-paste.ini
* /etc/keystone/keystone.conf
* /etc/nova/api-paste.ini
* /etc/swift/proxy-server.conf

There is no other custom configuration file.

=============
Configuration
=============

Keystone
========

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

Nova
====

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

Swift
=====

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



Revision: _sha1_

Build date: |today|