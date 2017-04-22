# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.


import moon_db
import uuid

Connector = moon_db.Driver("sql", "mysql+pymysql://moonuser:password@localhost/moon")
Connector.driver.init_db()


def create_intra_extension(policy_model="policy_authz"):
    ie = dict()
    ie['id'] = uuid.uuid4().hex
    ie["name"] = "test IE " + uuid.uuid4().hex
    ie["policymodel"] = "policy_authz"
    ie["description"] = "a simple description."
    ie["model"] = policy_model
    genre = "admin"
    if "authz" in policy_model:
        genre = "authz"
    ie["genre"] = genre
    # ref = self.admin_api.load_intra_extension_dict(self.root_api.root_admin_id,
    #                                                intra_extension_dict=ie)
    # self.admin_api.populate_default_data(ref)
    return ie


def test_get_intraextension():
    t = Connector.driver.get_intra_extensions_dict()
    assert type(t) == dict


def test_set_intra_extension():
    number_of_ie = len(Connector.driver.get_intra_extensions_dict())
    ie = create_intra_extension()
    data = Connector.driver.set_intra_extension_dict(ie['id'], ie)
    assert type(data) == dict
    assert len(Connector.driver.get_intra_extensions_dict()) == number_of_ie+1


# TODO (dthom): all tests can be got from keystone-moon
