# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import moon_db
import uuid

Connector = moon_db.Driver("sql", "mysql+pymysql://moonuser:password@localhost/moon")
Connector.driver.init_db()


def test_get_tenants():
    t = Connector.driver.get_tenants_dict()
    print(t)
    assert type(t) == dict


def test_add_tenant():
    new_tenant = {
        "id": uuid.uuid4().hex,
        "name": "demo",
        "description": uuid.uuid4().hex,
        "intra_authz_extension_id": "",
        "intra_admin_extension_id": "",
    }
    data = Connector.driver.add_tenant_dict(tenant_id=new_tenant['id'],
                                            tenant_dict=new_tenant)
    data_id = list(data.keys())[0]
    assert new_tenant["id"] == data_id
    assert new_tenant["name"] == data[data_id]["name"]
    assert new_tenant["intra_authz_extension_id"] == data[data_id]["intra_authz_extension_id"]
    assert new_tenant["intra_admin_extension_id"] == data[data_id]["intra_admin_extension_id"]
    data = Connector.driver.get_tenants_dict()
    assert data != {}


def test_del_tenant():
    new_tenant = {
        "id": uuid.uuid4().hex,
        "name": "demo",
        "description": uuid.uuid4().hex,
        "intra_authz_extension_id": "",
        "intra_admin_extension_id": "",
    }
    data = Connector.driver.get_tenants_dict()
    number_of_tenant = len(data.keys())
    data = Connector.driver.add_tenant_dict(tenant_id=new_tenant['id'],
                                            tenant_dict=new_tenant)
    data_id = list(data.keys())[0]
    assert new_tenant["name"] == data[data_id]["name"]
    assert new_tenant["intra_authz_extension_id"] == data[data_id]["intra_authz_extension_id"]
    assert new_tenant["intra_admin_extension_id"] == data[data_id]["intra_admin_extension_id"]
    data = Connector.driver.get_tenants_dict()
    assert len(data.keys()) == number_of_tenant+1
    Connector.driver.del_tenant(data_id)
    data = Connector.driver.get_tenants_dict()
    assert len(data.keys()) == number_of_tenant


def test_set_tenant():
    new_tenant = {
        "id": uuid.uuid4().hex,
        "name": "demo",
        "description": uuid.uuid4().hex,
        "intra_authz_extension_id": "123456",
        "intra_admin_extension_id": "0987654",
    }
    data = Connector.driver.get_tenants_dict()
    number_of_tenant = len(data.keys())
    data = Connector.driver.add_tenant_dict(tenant_id=new_tenant['id'],
                                            tenant_dict=new_tenant)
    data_id = list(data.keys())[0]
    assert new_tenant["name"] == data[data_id]["name"]
    assert new_tenant["intra_authz_extension_id"] == data[data_id]["intra_authz_extension_id"]
    assert new_tenant["intra_admin_extension_id"] == data[data_id]["intra_admin_extension_id"]
    data = Connector.driver.get_tenants_dict()
    assert len(data.keys()) == number_of_tenant+1

    new_tenant["name"] = "demo2"
    data = Connector.driver.set_tenant_dict(tenant_id=data_id, tenant_dict=new_tenant)
    data_id = list(data.keys())[0]
    assert new_tenant["name"] == data[data_id]["name"]
    assert new_tenant["intra_authz_extension_id"] == data[data_id]["intra_authz_extension_id"]
    assert new_tenant["intra_admin_extension_id"] == data[data_id]["intra_admin_extension_id"]

