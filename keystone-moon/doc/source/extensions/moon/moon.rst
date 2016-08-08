..
      Copyright 2015 Orange
      All Rights Reserved.

      Licensed under the Apache License, Version 2.0 (the "License"); you may
      not use this file except in compliance with the License. You may obtain
      a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

      Unless required by applicable law or agreed to in writing, software
      distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
      WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
      License for the specific language governing permissions and limitations
      under the License.

============
Moon backend
============

Before doing anything, you must test your installation and check that your infrastructure is working.
For example, check that you can create new virtual machines with admin and demo login.

Configuration
-------------

Moon is a contribute backend so you have to enable it by modifying /etc/keystone/keystone-paste.ini, like this:

.. code-block:: ini

    [pipeline:moon_pipeline]
    pipeline = sizelimit url_normalize request_id build_auth_context token_auth admin_token_auth json_body ec2_extension_v3 s3_extension moon_service

    [app:moon_service]
    use = egg:keystone#moon_service

    ...

    [composite:main]
    use = egg:Paste#urlmap
    /moon = moon_pipeline
    /v2.0 = public_api
    /v3 = api_v3
    / = public_version_api

    [composite:admin]
    use = egg:Paste#urlmap
    /moon = moon_pipeline
    /v2.0 = admin_api
    /v3 = api_v3
    / = admin_version_api

    ...

You must modify /etc/keystone/keystone.conf as you need (see at the end of the file) and copy the following directories:

.. code-block:: sh

    cp -R /opt/stack/keystone/examples/moon/policies/ /etc/keystone/
    cp -R /opt/stack/keystone/examples/moon/super_extension/ /etc/keystone/

You can now update the Keystone database and create the directory for logs and restart the Keystone service:

.. code-block:: sh

    cd /opt/stack/keystone
    ./bin/keystone-manage db_sync --extension moon
    sudo mkdir /var/log/moon/
    sudo chown vagrant /var/log/moon/
    sudo service apache2 restart

You have to install our version of keystonemiddleware https://github.com/rebirthmonkey/keystonemiddleware :

.. code-block:: sh

    cd
    git clone https://github.com/rebirthmonkey/keystonemiddleware.git
    cd keystonemiddleware
    sudo python setup.py install

At this time, the only method to configure Moon is to use the python-moonclient which is a console based client:

.. code-block:: sh

    cd
    git clone https://github.com/rebirthmonkey/moonclient.git
    cd moonclient
    sudo python setup.py install

If afterwards, you have some problem restarting nova-api, try removing the package python-six:

.. code-block:: sh

    sudo apt-get remove python-six


Nova must be configured to send request to Keystone, you have to modify /etc/nova/api-paste.ini :

.. code-block:: ini

    ...

    [composite:openstack_compute_api_v2]
    use = call:nova.api.auth:pipeline_factory
    noauth = compute_req_id faultwrap sizelimit noauth ratelimit osapi_compute_app_v2
    noauth2 = compute_req_id faultwrap sizelimit noauth2 ratelimit osapi_compute_app_v2
    keystone = compute_req_id faultwrap sizelimit authtoken keystonecontext moon ratelimit osapi_compute_app_v2
    keystone_nolimit = compute_req_id faultwrap sizelimit authtoken keystonecontext moon osapi_compute_app_v2

    [composite:openstack_compute_api_v21]
    use = call:nova.api.auth:pipeline_factory_v21
    noauth = compute_req_id faultwrap sizelimit noauth osapi_compute_app_v21
    noauth2 = compute_req_id faultwrap sizelimit noauth2 osapi_compute_app_v21
    keystone = compute_req_id faultwrap sizelimit authtoken keystonecontext moon osapi_compute_app_v21

    [composite:openstack_compute_api_v3]
    use = call:nova.api.auth:pipeline_factory_v21
    noauth = request_id faultwrap sizelimit noauth_v3 osapi_compute_app_v3
    noauth2 = request_id faultwrap sizelimit noauth_v3 osapi_compute_app_v3
    keystone = request_id faultwrap sizelimit authtoken keystonecontext moon osapi_compute_app_v3

    ...

    [filter:moon]
    paste.filter_factory = keystonemiddleware.authz:filter_factory

If Swift is also installed, you have to configured it, in /etc/swift/proxy-server.conf :

.. code-block:: ini

    ...

    [pipeline:main]
    pipeline = catch_errors gatekeeper healthcheck proxy-logging cache container_sync bulk tempurl ratelimit crossdomain authtoken keystoneauth tempauth  formpost staticweb container-quotas account-quotas slo dlo proxy-logging moon proxy-server

    ...

    [filter:moon]
    paste.filter_factory = keystonemiddleware.authz:filter_factory

Nova and Swift must be restarted after that, depending on your configuration, you will have to use 'screen' (if using devstack)
or 'service' on those daemons : nova-api and swift-proxy

Usage
-----

TODO