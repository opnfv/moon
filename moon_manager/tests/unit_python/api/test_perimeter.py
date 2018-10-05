# import moon_manager
# import moon_manager.api
import json
import api.utilities as utilities
from helpers import data_builder as builder
import helpers.policy_helper as policy_helper
from uuid import uuid4


def get_subjects(client):
    req = client.get("/subjects")
    subjects = utilities.get_json(req.data)
    return req, subjects


def add_subjects(client, policy_id, name, perimeter_id=None, data=None):
    if not data:
        name = name + uuid4().hex
        data = {
            "name": name,
            "description": "description of {}".format(name),
            "password": "password for {}".format(name),
            "email": "{}@moon".format(name)
        }
    if not perimeter_id:
        req = client.post("/policies/{}/subjects".format(policy_id), data=json.dumps(data),
                          headers={'Content-Type': 'application/json'})
    else:
        req = client.post("/policies/{}/subjects/{}".format(policy_id, perimeter_id),
                          data=json.dumps(
                              data),
                          headers={'Content-Type': 'application/json'})
    subjects = utilities.get_json(req.data)
    return req, subjects


def delete_subjects_without_perimeter_id(client):
    req = client.delete("/subjects/{}".format(""))
    return req


def test_perimeter_get_subject():
    client = utilities.register_client()
    req, subjects = get_subjects(client)
    assert req.status_code == 200
    assert isinstance(subjects, dict)
    assert "subjects" in subjects


def test_perimeter_add_subject():
    client = utilities.register_client()
    policies = policy_helper.add_policies()
    policy_id = list(policies.keys())[0]

    req, subjects = add_subjects(client, policy_id, "testuser")
    value = list(subjects["subjects"].values())[0]
    assert req.status_code == 200
    assert value["name"]
    assert value["email"]


def test_perimeter_add_same_subject_perimeter_id_with_new_policy_id():
    client = utilities.register_client()
    policies1 = policy_helper.add_policies()
    policy_id1 = list(policies1.keys())[0]
    name = "testuser"
    perimeter_id = uuid4().hex
    data = {
        "name": name + uuid4().hex,
        "description": "description of {}".format(name),
        "password": "password for {}".format(name),
        "email": "{}@moon".format(name)
    }
    add_subjects(client, policy_id1, data['name'], perimeter_id=perimeter_id, data=data)
    policies2 = policy_helper.add_policies()
    policy_id2 = list(policies2.keys())[0]
    req, subjects = add_subjects(client, policy_id2, data['name'],
                                 perimeter_id=perimeter_id, data=data)
    value = list(subjects["subjects"].values())[0]
    assert req.status_code == 200
    assert value["name"]
    assert value["email"]
    assert len(value['policy_list']) == 2
    assert policy_id1 in value['policy_list']
    assert policy_id2 in value['policy_list']


def test_perimeter_add_same_subject_perimeter_id_with_different_name():
    client = utilities.register_client()
    policies1 = policy_helper.add_policies()
    policy_id1 = list(policies1.keys())[0]
    perimeter_id = uuid4().hex
    add_subjects(client, policy_id1, "testuser", perimeter_id=perimeter_id)
    policies2 = policy_helper.add_policies()
    policy_id2 = list(policies2.keys())[0]
    req, subjects = add_subjects(client, policy_id2, "testuser", perimeter_id=perimeter_id)
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == '400: Perimeter content is invalid.'


def test_perimeter_add_same_subject_name_with_new_policy_id():
    client = utilities.register_client()
    policies1 = policy_helper.add_policies()
    policy_id1 = list(policies1.keys())[0]
    perimeter_id = uuid4().hex
    name = "testuser" + uuid4().hex
    data = {
        "name": name,
        "description": "description of {}".format(name),
        "password": "password for {}".format(name),
        "email": "{}@moon".format(name)
    }
    req, subjects = add_subjects(client, policy_id1, None, perimeter_id=perimeter_id,
                                 data=data)
    policies2 = policy_helper.add_policies()
    policy_id2 = list(policies2.keys())[0]
    value = list(subjects["subjects"].values())[0]
    data = {
        "name": value['name'],
        "description": "description of {}".format(value['name']),
        "password": "password for {}".format(value['name']),
        "email": "{}@moon".format(value['name'])
    }
    req, subjects = add_subjects(client, policy_id2, None, data=data)
    value = list(subjects["subjects"].values())[0]
    assert req.status_code == 200
    assert value["name"]
    assert value["email"]
    assert len(value['policy_list']) == 2
    assert policy_id1 in value['policy_list']
    assert policy_id2 in value['policy_list']


def test_perimeter_add_same_subject_name_with_same_policy_id():
    client = utilities.register_client()
    policies1 = policy_helper.add_policies()
    policy_id1 = list(policies1.keys())[0]
    perimeter_id = uuid4().hex
    name = "testuser" + uuid4().hex
    data = {
        "name": name,
        "description": "description of {}".format(name),
        "password": "password for {}".format(name),
        "email": "{}@moon".format(name)
    }
    req, subjects = add_subjects(client, policy_id1, None, perimeter_id=perimeter_id,
                                 data=data)
    value = list(subjects["subjects"].values())[0]
    data = {
        "name": value['name'],
        "description": "description of {}".format(value['name']),
        "password": "password for {}".format(value['name']),
        "email": "{}@moon".format(value['name'])
    }
    req, subjects = add_subjects(client, policy_id1, None, data=data)
    assert req.status_code == 409
    assert json.loads(req.data)["message"] == '409: Policy Already Exists'


def test_perimeter_add_same_subject_perimeter_id_with_existed_policy_id_in_list():
    client = utilities.register_client()
    policies = policy_helper.add_policies()
    policy_id = list(policies.keys())[0]
    name = "testuser" + uuid4().hex
    data = {
        "name": name,
        "description": "description of {}".format(name),
        "password": "password for {}".format(name),
        "email": "{}@moon".format(name)
    }
    req, subjects = add_subjects(client, policy_id, name, data=data)
    perimeter_id = list(subjects["subjects"].values())[0]['id']
    req, subjects = add_subjects(client, policy_id, name, perimeter_id=perimeter_id, data=data)
    assert req.status_code == 409
    assert json.loads(req.data)["message"] == '409: Policy Already Exists'


def test_perimeter_add_subject_invalid_policy_id():
    client = utilities.register_client()
    policies = policy_helper.add_policies()
    policy_id = list(policies.keys())[0]
    name = "testuser"
    data = {
        "name": name + uuid4().hex,
        "description": "description of {}".format(name),
        "password": "password for {}".format(name),
        "email": "{}@moon".format(name)
    }
    req, subjects = add_subjects(client, policy_id + "0", "testuser", data)
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == '400: Policy Unknown'


def test_perimeter_add_subject_policy_id_none():
    client = utilities.register_client()
    name = "testuser"
    data = {
        "name": name + uuid4().hex,
        "description": "description of {}".format(name),
        "password": "password for {}".format(name),
        "email": "{}@moon".format(name)
    }
    req, subjects = add_subjects(client, None, "testuser", data)
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == '400: Policy Unknown'


def test_perimeter_add_subject_with_forbidden_char_in_name():
    client = utilities.register_client()
    data = {
        "name": "<a>",
        "description": "description of {}".format(""),
        "password": "password for {}".format(""),
        "email": "{}@moon".format("")
    }
    req = client.post("/policies/{}/subjects".format("111"), data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == "Key: 'name', [Forbidden characters in string]"


def test_perimeter_update_subject_name():
    client = utilities.register_client()
    policies = policy_helper.add_policies()
    policy_id = list(policies.keys())[0]
    req, subjects = add_subjects(client, policy_id, "testuser")
    value1 = list(subjects["subjects"].values())[0]
    perimeter_id = value1['id']
    data = {
        'name': value1['name'] + "update"
    }
    req = client.patch("/subjects/{}".format(perimeter_id), data=json.dumps(data),
                       headers={'Content-Type': 'application/json'})
    subjects = utilities.get_json(req.data)
    value2 = list(subjects["subjects"].values())[0]
    assert req.status_code == 200
    assert value1['name'] + 'update' == value2['name']
    assert value1['id'] == value2['id']
    assert value1['description'] == value2['description']


def test_perimeter_update_subject_description():
    client = utilities.register_client()
    policies = policy_helper.add_policies()
    policy_id = list(policies.keys())[0]
    req, subjects = add_subjects(client, policy_id, "testuser")
    value1 = list(subjects["subjects"].values())[0]
    perimeter_id = value1['id']
    data = {
        'description': value1['description'] + "update",
    }
    req = client.patch("/subjects/{}".format(perimeter_id), data=json.dumps(data),
                       headers={'Content-Type': 'application/json'})
    subjects = utilities.get_json(req.data)
    value2 = list(subjects["subjects"].values())[0]
    assert req.status_code == 200
    assert value1['name'] == value2['name']
    assert value1['id'] == value2['id']
    assert value1['description'] + 'update' == value2['description']


def test_perimeter_update_subject_description_and_name():
    client = utilities.register_client()
    policies = policy_helper.add_policies()
    policy_id = list(policies.keys())[0]

    req, subjects = add_subjects(client, policy_id, "testuser")
    value1 = list(subjects["subjects"].values())[0]
    perimeter_id = value1['id']
    data = {
        'description': value1['description'] + "update",
        'name': value1['name'] + "update"
    }
    req = client.patch("/subjects/{}".format(perimeter_id), data=json.dumps(data),
                       headers={'Content-Type': 'application/json'})
    subjects = utilities.get_json(req.data)
    value2 = list(subjects["subjects"].values())[0]
    assert req.status_code == 200
    assert value1['name'] + 'update' == value2['name']
    assert value1['id'] == value2['id']
    assert value1['description'] + 'update' == value2['description']


def test_perimeter_update_subject_wrong_id():
    client = utilities.register_client()
    name = 'testuser' + uuid4().hex
    policies1 = policy_helper.add_policies()
    policy_id1 = list(policies1.keys())[0]
    data = {
        "name": name,
        "description": "description of {}".format('testuser'),
    }
    req, subjects = add_subjects(client, policy_id=policy_id1, name='testuser', data=data)
    value1 = list(subjects["subjects"].values())[0]
    perimeter_id = value1['id']
    data = {
        'name': value1['name'] + "update",
        'description': value1['description'] + "update"
    }
    req = client.patch("/subjects/{}".format(perimeter_id + "wrong"), data=json.dumps(data),
                       headers={'Content-Type': 'application/json'})
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == '400: Perimeter content is invalid.'


def test_perimeter_update_subject_name_with_existed_one():
    client = utilities.register_client()
    name1 = 'testuser' + uuid4().hex
    policies1 = policy_helper.add_policies()
    policy_id1 = list(policies1.keys())[0]
    perimeter_id1 = uuid4().hex
    req, subjects = add_subjects(client, policy_id=policy_id1, name=name1,
                                 perimeter_id=perimeter_id1)
    value1 = list(subjects["subjects"].values())[0]
    perimeter_id2 = uuid4().hex
    name2 = 'testuser' + uuid4().hex
    req, subjects = add_subjects(client, policy_id=policy_id1, name=name2,
                                 perimeter_id=perimeter_id2)
    data = {
        'name': value1['name'],
    }
    req = client.patch("/subjects/{}".format(perimeter_id2), data=json.dumps(data),
                       headers={'Content-Type': 'application/json'})
    assert req.status_code == 409


def test_perimeter_delete_subject():
    client = utilities.register_client()
    policies = policy_helper.add_policies()
    policy_id = list(policies.keys())[0]
    req, subjects = add_subjects(client, policy_id, "testuser")
    subject_id = list(subjects["subjects"].values())[0]["id"]
    req = client.delete("/policies/{}/subjects/{}".format(policy_id, subject_id))
    assert req.status_code == 200


def test_perimeter_delete_subjects_without_perimeter_id():
    client = utilities.register_client()
    req = delete_subjects_without_perimeter_id(client)
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == "400: Subject Unknown"


def get_objects(client):
    req = client.get("/objects")
    objects = utilities.get_json(req.data)
    return req, objects


def add_objects(client, name, policyId=None, data=None, perimeter_id=None):
    if not policyId:
        subject_category_id, object_category_id, action_category_id, meta_rule_id, policyId = builder.create_new_policy(
            subject_category_name="subject_category1" + uuid4().hex,
            object_category_name="object_category1" + uuid4().hex,
            action_category_name="action_category1" + uuid4().hex,
            meta_rule_name="meta_rule_1" + uuid4().hex,
            model_name="model1" + uuid4().hex)
    if not data:
        data = {
            "name": name + uuid4().hex,
            "description": "description of {}".format(name),
        }
    if not perimeter_id:
        req = client.post("/policies/{}/objects/".format(policyId), data=json.dumps(data),
                          headers={'Content-Type': 'application/json'})
    else:
        req = client.post("/policies/{}/objects/{}".format(policyId, perimeter_id),
                          data=json.dumps(data),
                          headers={'Content-Type': 'application/json'})
    objects = utilities.get_json(req.data)
    return req, objects


def delete_objects_without_perimeter_id(client):
    req = client.delete("/objects/{}".format(""))
    return req


def test_perimeter_get_object():
    client = utilities.register_client()
    req, objects = get_objects(client)
    assert req.status_code == 200
    assert isinstance(objects, dict)
    assert "objects" in objects


def test_perimeter_add_object():
    client = utilities.register_client()
    req, objects = add_objects(client, "testuser")
    value = list(objects["objects"].values())[0]
    assert req.status_code == 200
    assert value['name']


def test_perimeter_add_object_with_wrong_policy_id():
    client = utilities.register_client()
    req, objects = add_objects(client, "testuser", policyId='wrong')
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == '400: Policy Unknown'


def test_perimeter_add_object_with_policy_id_none():
    client = utilities.register_client()
    data = {
        "name": "testuser" + uuid4().hex,
        "description": "description of {}".format("testuser"),
    }
    req = client.post("/policies/{}/objects/".format(None), data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == '400: Policy Unknown'


def test_perimeter_add_same_object_name_with_new_policy_id():
    client = utilities.register_client()
    req, objects = add_objects(client, "testuser")
    value1 = list(objects["objects"].values())[0]
    policies1 = policy_helper.add_policies()
    policy_id1 = list(policies1.keys())[0]
    data = {
        "name": value1['name'],
        "description": "description of {}".format('testuser'),
    }
    req, objects = add_objects(client, 'testuser', policyId=policy_id1, data=data)
    value2 = list(objects["objects"].values())[0]
    assert req.status_code == 200
    assert value1['id'] == value2['id']
    assert value1['name'] == value2['name']


def test_perimeter_add_same_object_perimeter_id_with_new_policy_id():
    client = utilities.register_client()
    req, objects = add_objects(client, "testuser")
    value1 = list(objects["objects"].values())[0]
    policies1 = policy_helper.add_policies()
    policy_id1 = list(policies1.keys())[0]
    data = {
        "name": value1['name'],
        "description": "description of {}".format('testuser'),
    }
    req, objects = add_objects(client, 'testuser', policyId=policy_id1, data=data,
                               perimeter_id=value1['id'])
    value2 = list(objects["objects"].values())[0]
    assert req.status_code == 200
    assert value1['id'] == value2['id']
    assert value1['name'] == value2['name']


def test_perimeter_add_same_object_perimeter_id_with_different_name():
    client = utilities.register_client()
    req, objects = add_objects(client, "testuser")
    value1 = list(objects["objects"].values())[0]
    policies1 = policy_helper.add_policies()
    policy_id1 = list(policies1.keys())[0]
    data = {
        "name": value1['name'] + 'different',
        "description": "description of {}".format('testuser'),
    }
    req, objects = add_objects(client, 'testuser', policyId=policy_id1, data=data,
                               perimeter_id=value1['id'])
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == '400: Perimeter content is invalid.'


def test_perimeter_add_same_object_name_with_same_policy_id():
    client = utilities.register_client()
    name = 'testuser' + uuid4().hex
    policies1 = policy_helper.add_policies()
    policy_id1 = list(policies1.keys())[0]
    data = {
        "name": name,
        "description": "description of {}".format('testuser'),
    }
    req, objects = add_objects(client, 'testuser', policyId=policy_id1, data=data)
    value = list(objects["objects"].values())[0]
    assert req.status_code == 200
    req, objects = add_objects(client, 'testuser', policyId=policy_id1, data=data)
    assert req.status_code == 409
    assert json.loads(req.data)["message"] == '409: Policy Already Exists'


def test_perimeter_add_same_object_perimeter_id_with_existed_policy_id_in_list():
    client = utilities.register_client()
    name = 'testuser' + uuid4().hex
    policies1 = policy_helper.add_policies()
    policy_id1 = list(policies1.keys())[0]
    data = {
        "name": name,
        "description": "description of {}".format('testuser'),
    }
    req, objects = add_objects(client, 'testuser', policyId=policy_id1, data=data)
    value = list(objects["objects"].values())[0]
    req, objects = add_objects(client, 'testuser', policyId=policy_id1, data=data,
                               perimeter_id=value['id'])
    assert req.status_code == 409
    assert json.loads(req.data)["message"] == '409: Policy Already Exists'


def test_perimeter_update_object_name():
    client = utilities.register_client()
    name = 'testuser' + uuid4().hex
    policies1 = policy_helper.add_policies()
    policy_id1 = list(policies1.keys())[0]
    data = {
        "name": name,
        "description": "description of {}".format('testuser'),
    }
    req, objects = add_objects(client, 'testuser', policyId=policy_id1, data=data)

    value1 = list(objects["objects"].values())[0]
    perimeter_id = value1['id']
    data = {
        'name': value1['name'] + "update"
    }
    req = client.patch("/objects/{}".format(perimeter_id), data=json.dumps(data),
                       headers={'Content-Type': 'application/json'})

    objects = utilities.get_json(req.data)
    value2 = list(objects["objects"].values())[0]
    assert req.status_code == 200
    assert value1['name'] + 'update' == value2['name']
    assert value1['id'] == value2['id']
    assert value1['description'] == value2['description']


def test_perimeter_update_object_description():
    client = utilities.register_client()
    name = 'testuser' + uuid4().hex
    policies1 = policy_helper.add_policies()
    policy_id1 = list(policies1.keys())[0]
    data = {
        "name": name,
        "description": "description of {}".format('testuser'),
    }
    req, objects = add_objects(client, 'testuser', policyId=policy_id1, data=data)

    value1 = list(objects["objects"].values())[0]
    perimeter_id = value1['id']
    data = {
        'description': value1['description'] + "update"
    }
    req = client.patch("/objects/{}".format(perimeter_id), data=json.dumps(data),
                       headers={'Content-Type': 'application/json'})

    objects = utilities.get_json(req.data)
    value2 = list(objects["objects"].values())[0]
    assert req.status_code == 200
    assert value1['name'] == value2['name']
    assert value1['id'] == value2['id']
    assert value1['description'] + 'update' == value2['description']


def test_perimeter_update_object_description_and_name():
    client = utilities.register_client()
    name = 'testuser' + uuid4().hex
    policies1 = policy_helper.add_policies()
    policy_id1 = list(policies1.keys())[0]
    data = {
        "name": name,
        "description": "description of {}".format('testuser'),
    }
    req, objects = add_objects(client, 'testuser', policyId=policy_id1, data=data)

    value1 = list(objects["objects"].values())[0]
    perimeter_id = value1['id']
    data = {
        'name': value1['name'] + "update",
        'description': value1['description'] + "update"
    }
    req = client.patch("/objects/{}".format(perimeter_id), data=json.dumps(data),
                       headers={'Content-Type': 'application/json'})

    objects = utilities.get_json(req.data)
    value2 = list(objects["objects"].values())[0]
    assert req.status_code == 200
    assert value1['name'] + 'update' == value2['name']
    assert value1['id'] == value2['id']
    assert value1['description'] + 'update' == value2['description']


def test_perimeter_update_object_wrong_id():
    client = utilities.register_client()
    name = 'testuser' + uuid4().hex
    policies1 = policy_helper.add_policies()
    policy_id1 = list(policies1.keys())[0]
    data = {
        "name": name,
        "description": "description of {}".format('testuser'),
    }
    req, objects = add_objects(client, 'testuser', policyId=policy_id1, data=data)

    value1 = list(objects["objects"].values())[0]
    perimeter_id = value1['id']
    data = {
        'name': value1['name'] + "update",
        'description': value1['description'] + "update"
    }
    req = client.patch("/objects/{}".format(perimeter_id + "wrong"), data=json.dumps(data),
                       headers={'Content-Type': 'application/json'})
    assert req.status_code == 400


def test_perimeter_update_object_name_with_existed_one():
    client = utilities.register_client()
    name = 'testuser' + uuid4().hex
    policies1 = policy_helper.add_policies()
    policy_id1 = list(policies1.keys())[0]
    data1 = {
        "name": name,
        "description": "description of {}".format('testuser'),
    }
    req, objects = add_objects(client, 'testuser', policyId=policy_id1, data=data1)
    value1 = list(objects["objects"].values())[0]

    name = 'testuser' + uuid4().hex

    data2 = {
        "name": name,
        "description": "description of {}".format('testuser'),
    }
    req, objects = add_objects(client, 'testuser', policyId=policy_id1, data=data2)

    value2 = list(objects["objects"].values())[0]
    perimeter_id2 = value2['id']

    data3 = {
        'name': value1['name']
    }
    req = client.patch("/objects/{}".format(perimeter_id2), data=json.dumps(data3),
                       headers={'Content-Type': 'application/json'})
    assert req.status_code == 409
    assert json.loads(req.data)["message"] == '409: Object Existing'


def test_perimeter_add_object_without_name():
    client = utilities.register_client()
    data = {
        "name": "<br/>",
        "description": "description of {}".format(""),
    }
    req = client.post("/policies/{}/objects/".format("111"), data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == "Key: 'name', [Forbidden characters in string]"


def test_perimeter_add_object_with_name_contain_spaces():
    client = utilities.register_client()
    data = {
        "name": "test<a>user",
        "description": "description of {}".format("test user"),
    }
    req = client.post("/policies/{}/objects/".format("111"), data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == "Key: 'name', [Forbidden characters in string]"


def test_perimeter_delete_object():
    client = utilities.register_client()
    policies = policy_helper.add_policies()
    policy_id = list(policies.keys())[0]
    object_id = builder.create_object(policy_id)
    req = client.delete("/policies/{}/objects/{}".format(policy_id, object_id))
    assert req.status_code == 200


def test_perimeter_delete_objects_without_perimeter_id():
    client = utilities.register_client()
    req = delete_objects_without_perimeter_id(client)
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == "400: Object Unknown"


def get_actions(client):
    req = client.get("/actions")
    actions = utilities.get_json(req.data)
    return req, actions


def add_actions(client, name, policy_id=None, data=None, perimeter_id=None):
    if not policy_id:
        subject_category_id, object_category_id, action_category_id, meta_rule_id, policy_id = builder.create_new_policy(
            subject_category_name="subject_category1" + uuid4().hex,
            object_category_name="object_category1" + uuid4().hex,
            action_category_name="action_category1" + uuid4().hex,
            meta_rule_name="meta_rule_1" + uuid4().hex,
            model_name="model1" + uuid4().hex)

    if not data:
        data = {
            "name": name + uuid4().hex,
            "description": "description of {}".format(name),
        }
    if not perimeter_id:
        req = client.post("/policies/{}/actions/".format(policy_id), data=json.dumps(data),
                          headers={'Content-Type': 'application/json'})
    else:
        req = client.post("/policies/{}/actions/{}".format(policy_id, perimeter_id),
                          data=json.dumps(data),
                          headers={'Content-Type': 'application/json'})

    actions = utilities.get_json(req.data)
    return req, actions


def delete_actions_without_perimeter_id(client):
    req = client.delete("/actions/{}".format(""))
    return req


def test_perimeter_get_actions():
    client = utilities.register_client()
    req, actions = get_actions(client)
    assert req.status_code == 200
    assert isinstance(actions, dict)
    assert "actions" in actions


def test_perimeter_add_actions():
    client = utilities.register_client()
    req, actions = add_actions(client, "testuser")
    value = list(actions["actions"].values())[0]
    assert req.status_code == 200
    assert value['name']


def test_perimeter_add_action_with_wrong_policy_id():
    client = utilities.register_client()
    req, actions = add_actions(client, "testuser", policy_id="wrong")
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == '400: Policy Unknown'


def test_perimeter_add_action_with_policy_id_none():
    client = utilities.register_client()
    data = {
        "name": "testuser" + uuid4().hex,
        "description": "description of {}".format("testuser"),
    }
    req = client.post("/policies/{}/actions/".format(None), data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == '400: Policy Unknown'


def test_perimeter_add_same_action_name_with_new_policy_id():
    client = utilities.register_client()
    req, action = add_actions(client, "testuser")
    value1 = list(action["actions"].values())[0]
    policies1 = policy_helper.add_policies()
    policy_id1 = list(policies1.keys())[0]
    data = {
        "name": value1['name'],
        "description": "description of {}".format('testuser'),
    }
    req, action = add_actions(client, 'testuser', policy_id=policy_id1, data=data)
    value2 = list(action["actions"].values())[0]
    assert req.status_code == 200
    assert value1['id'] == value2['id']
    assert value1['name'] == value2['name']


def test_perimeter_add_same_action_perimeter_id_with_new_policy_id():
    client = utilities.register_client()
    req, action = add_actions(client, "testuser")
    value1 = list(action["actions"].values())[0]
    policies1 = policy_helper.add_policies()
    policy_id1 = list(policies1.keys())[0]
    data = {
        "name": value1['name'],
        "description": "description of {}".format('testuser'),
    }
    req, action = add_actions(client, 'testuser', policy_id=policy_id1, data=data,
                              perimeter_id=value1['id'])
    value2 = list(action["actions"].values())[0]
    assert req.status_code == 200
    assert value1['id'] == value2['id']
    assert value1['name'] == value2['name']


def test_perimeter_add_same_action_perimeter_id_with_different_name():
    client = utilities.register_client()
    req, action = add_actions(client, "testuser")
    value1 = list(action["actions"].values())[0]
    policies1 = policy_helper.add_policies()
    policy_id1 = list(policies1.keys())[0]
    data = {
        "name": value1['name'] + 'different',
        "description": "description of {}".format('testuser'),
    }
    req, action = add_actions(client, 'testuser', policy_id=policy_id1, data=data,
                              perimeter_id=value1['id'])
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == '400: Perimeter content is invalid.'


def test_perimeter_add_same_action_name_with_same_policy_id():
    client = utilities.register_client()
    policies1 = policy_helper.add_policies()
    policy_id1 = list(policies1.keys())[0]
    req, action = add_actions(client, "testuser", policy_id=policy_id1)
    value1 = list(action["actions"].values())[0]
    data = {
        "name": value1['name'],
        "description": "description of {}".format('testuser'),
    }
    req, action = add_actions(client, 'testuser', policy_id=policy_id1, data=data)
    assert req.status_code == 409
    assert json.loads(req.data)["message"] == '409: Policy Already Exists'


def test_perimeter_add_same_action_perimeter_id_with_existed_policy_id_in_list():
    client = utilities.register_client()
    policies1 = policy_helper.add_policies()
    policy_id1 = list(policies1.keys())[0]
    req, action = add_actions(client, "testuser", policy_id=policy_id1)
    value1 = list(action["actions"].values())[0]
    data = {
        "name": value1['name'],
        "description": "description of {}".format('testuser'),
    }
    req, action = add_actions(client, 'testuser', policy_id=policy_id1, data=data,
                              perimeter_id=value1['id'])
    assert req.status_code == 409
    assert json.loads(req.data)["message"] == '409: Policy Already Exists'


def test_perimeter_add_actions_without_name():
    client = utilities.register_client()
    data = {
        "name": "<a>",
        "description": "description of {}".format(""),
    }
    req = client.post("/policies/{}/actions".format("111"), data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == "Key: 'name', [Forbidden characters in string]"


def test_perimeter_add_actions_with_name_contain_spaces():
    client = utilities.register_client()
    data = {
        "name": "test<a>user",
        "description": "description of {}".format("test user"),
    }
    req = client.post("/policies/{}/actions".format("111"), data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == "Key: 'name', [Forbidden characters in string]"


def test_add_subjects_without_policy_id():
    client = utilities.register_client()
    data = {
        "name": "testuser",
        "description": "description of {}".format("test user"),
    }
    req = client.post("/policies/{}/subjects".format("111"), data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == "400: Policy Unknown"


def test_add_objects_without_policy_id():
    client = utilities.register_client()
    data = {
        "name": "testuser",
        "description": "description of {}".format("test user"),
    }
    req = client.post("/policies/{}/objects".format("111"), data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == "400: Policy Unknown"


def test_add_action_without_policy_id():
    client = utilities.register_client()
    data = {
        "name": "testuser",
        "description": "description of {}".format("test user"),
    }
    req = client.post("/policies/{}/actions".format("111"), data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == "400: Policy Unknown"


def test_perimeter_update_action_name():
    client = utilities.register_client()
    req, actions = add_actions(client, "testuser")
    value1 = list(actions["actions"].values())[0]
    perimeter_id = value1['id']
    data = {
        'name': value1['name'] + "update"
    }
    req = client.patch("/actions/{}".format(perimeter_id), data=json.dumps(data),
                       headers={'Content-Type': 'application/json'})
    subjects = utilities.get_json(req.data)
    value2 = list(subjects["actions"].values())[0]
    assert req.status_code == 200
    assert value1['name'] + 'update' == value2['name']
    assert value1['id'] == value2['id']
    assert value1['description'] == value2['description']


def test_perimeter_update_actions_description():
    client = utilities.register_client()
    req, actions = add_actions(client, "testuser")
    value1 = list(actions["actions"].values())[0]
    perimeter_id = value1['id']
    data = {
        'description': value1['description'] + "update"
    }
    req = client.patch("/actions/{}".format(perimeter_id), data=json.dumps(data),
                       headers={'Content-Type': 'application/json'})
    subjects = utilities.get_json(req.data)
    value2 = list(subjects["actions"].values())[0]
    assert req.status_code == 200
    assert value1['name'] == value2['name']
    assert value1['id'] == value2['id']
    assert value1['description'] + 'update' == value2['description']


def test_perimeter_update_actions_description_and_name():
    client = utilities.register_client()
    req, actions = add_actions(client, "testuser")
    value1 = list(actions["actions"].values())[0]
    perimeter_id = value1['id']
    data = {
        'name': value1['name'] + "update",
        'description': value1['description'] + "update"
    }
    req = client.patch("/actions/{}".format(perimeter_id), data=json.dumps(data),
                       headers={'Content-Type': 'application/json'})
    subjects = utilities.get_json(req.data)
    value2 = list(subjects["actions"].values())[0]
    assert req.status_code == 200
    assert value1['name'] + 'update' == value2['name']
    assert value1['id'] == value2['id']
    assert value1['description'] + 'update' == value2['description']


def test_perimeter_update_action_wrong_id():
    client = utilities.register_client()
    req, actions = add_actions(client, "testuser")
    value1 = list(actions["actions"].values())[0]
    perimeter_id = value1['id']
    data = {
        'name': value1['name'] + "update",
        'description': value1['description'] + "update"
    }
    req = client.patch("/actions/{}".format(perimeter_id + "wrong"), data=json.dumps(data),
                       headers={'Content-Type': 'application/json'})
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == '400: Perimeter content is invalid.'


def test_perimeter_update_action_name_with_existed_one():
    client = utilities.register_client()
    req, actions = add_actions(client, "testuser")
    value1 = list(actions["actions"].values())[0]
    req, actions = add_actions(client, "testuser")
    value2 = list(actions["actions"].values())[0]
    perimeter_id2 = value2['id']
    data = {
        'name': value1['name'],
    }
    req = client.patch("/actions/{}".format(perimeter_id2), data=json.dumps(data),
                       headers={'Content-Type': 'application/json'})
    assert req.status_code == 409
    assert json.loads(req.data)["message"] == '409: Action Existing'


def test_perimeter_delete_actions():
    client = utilities.register_client()

    policies = policy_helper.add_policies()
    policy_id = list(policies.keys())[0]
    action_id = builder.create_action(policy_id)
    req = client.delete("/policies/{}/actions/{}".format(policy_id, action_id))
    assert req.status_code == 200


def test_delete_subject_without_policy():
    client = utilities.register_client()

    policies = policy_helper.add_policies()
    policy_id = list(policies.keys())[0]

    action_id = builder.create_action(policy_id)

    req = client.delete("/subjects/{}".format(action_id))
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == "400: Policy Unknown"


def test_delete_objects_without_policy():
    client = utilities.register_client()

    policies = policy_helper.add_policies()
    policy_id = list(policies.keys())[0]

    action_id = builder.create_action(policy_id)

    req = client.delete("/objects/{}".format(action_id))
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == "400: Policy Unknown"


def test_delete_actions_without_policy():
    client = utilities.register_client()

    policies = policy_helper.add_policies()
    policy_id = list(policies.keys())[0]

    action_id = builder.create_action(policy_id)

    req = client.delete("/actions/{}".format(action_id))
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == "400: Policy Unknown"


def test_perimeter_delete_actions_without_perimeter_id():
    client = utilities.register_client()
    req = delete_actions_without_perimeter_id(client)
    assert req.status_code == 400
    assert json.loads(req.data)["message"] == "400: Action Unknown"
