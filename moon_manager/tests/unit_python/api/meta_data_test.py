import json
import api.utilities as utilities

#subject_categories_test


def get_subject_categories(client):
    req = client.get("/subject_categories")
    subject_categories = utilities.get_json(req.data)
    return req, subject_categories


def add_subject_categories(client, name):
    data = {
        "name": name,
        "description": "description of {}".format(name)
    }
    req = client.post("/subject_categories", data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    subject_categories = utilities.get_json(req.data)
    return req, subject_categories


def delete_subject_categories(client, name):
    request, subject_categories = get_subject_categories(client)
    for key, value in subject_categories['subject_categories'].items():
        if value['name'] == name:
            req = client.delete("/subject_categories/{}".format(key))
            break
    return req


def delete_subject_categories_without_id(client):
    req = client.delete("/subject_categories/{}".format(""))
    return req


def test_get_subject_categories():
    client = utilities.register_client()
    req, subject_categories = get_subject_categories(client)
    assert req.status_code == 200
    assert isinstance(subject_categories, dict)
    assert "subject_categories" in subject_categories


def test_add_subject_categories():
    client = utilities.register_client()
    req, subject_categories = add_subject_categories(client, "testuser")
    assert req.status_code == 200
    assert isinstance(subject_categories, dict)
    value = list(subject_categories["subject_categories"].values())[0]
    assert "subject_categories" in subject_categories
    assert value['name'] == "testuser"
    assert value['description'] == "description of {}".format("testuser")


def test_delete_subject_categories():
    client = utilities.register_client()
    req = delete_subject_categories(client, "testuser")
    assert req.status_code == 200


def test_delete_subject_categories_without_id():
    client = utilities.register_client()
    req = delete_subject_categories_without_id(client)
    assert req.status_code == 500


#---------------------------------------------------------------------------
#object_categories_test

def get_object_categories(client):
    req = client.get("/object_categories")
    object_categories = utilities.get_json(req.data)
    return req, object_categories


def add_object_categories(client, name):
    data = {
        "name": name,
        "description": "description of {}".format(name)
    }
    req = client.post("/object_categories", data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    object_categories = utilities.get_json(req.data)
    return req, object_categories


def delete_object_categories(client, name):
    request, object_categories = get_object_categories(client)
    for key, value in object_categories['object_categories'].items():
        if value['name'] == name:
            req = client.delete("/object_categories/{}".format(key))
            break
    return req


def delete_object_categories_without_id(client):
    req = client.delete("/object_categories/{}".format(""))
    return req


def test_get_object_categories():
    client = utilities.register_client()
    req, object_categories = get_object_categories(client)
    assert req.status_code == 200
    assert isinstance(object_categories, dict)
    assert "object_categories" in object_categories


def test_add_object_categories():
    client = utilities.register_client()
    req, object_categories = add_object_categories(client, "testuser")
    assert req.status_code == 200
    assert isinstance(object_categories, dict)
    value = list(object_categories["object_categories"].values())[0]
    assert "object_categories" in object_categories
    assert value['name'] == "testuser"
    assert value['description'] == "description of {}".format("testuser")


def test_delete_object_categories():
    client = utilities.register_client()
    req = delete_object_categories(client, "testuser")
    assert req.status_code == 200


def test_delete_object_categories_without_id():
    client = utilities.register_client()
    req = delete_object_categories_without_id(client)
    assert req.status_code == 500


#---------------------------------------------------------------------------
#action_categories_test

def get_action_categories(client):
    req = client.get("/action_categories")
    action_categories = utilities.get_json(req.data)
    return req, action_categories


def add_action_categories(client, name):
    data = {
        "name": name,
        "description": "description of {}".format(name)
    }
    req = client.post("/action_categories", data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    action_categories = utilities.get_json(req.data)
    return req, action_categories


def delete_action_categories(client, name):
    request, action_categories = get_action_categories(client)
    for key, value in action_categories['action_categories'].items():
        if value['name'] == name:
            req = client.delete("/action_categories/{}".format(key))
            break
    return req


def delete_action_categories_without_id(client):
    req = client.delete("/action_categories/{}".format(""))
    return req


def test_get_action_categories():
    client = utilities.register_client()
    req, action_categories = get_action_categories(client)
    assert req.status_code == 200
    assert isinstance(action_categories, dict)
    assert "action_categories" in action_categories


def test_add_action_categories():
    client = utilities.register_client()
    req, action_categories = add_action_categories(client, "testuser")
    assert req.status_code == 200
    assert isinstance(action_categories, dict)
    value = list(action_categories["action_categories"].values())[0]
    assert "action_categories" in action_categories
    assert value['name'] == "testuser"
    assert value['description'] == "description of {}".format("testuser")


def test_delete_action_categories():
    client = utilities.register_client()
    req = delete_action_categories(client, "testuser")
    assert req.status_code == 200


def test_delete_action_categories_without_id():
    client = utilities.register_client()
    req = delete_action_categories_without_id(client)
    assert req.status_code == 500
