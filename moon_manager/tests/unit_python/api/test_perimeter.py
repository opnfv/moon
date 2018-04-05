# import moon_manager
# import moon_manager.api
import json
import api.utilities as utilities


def get_subjects(client):
    req = client.get("/subjects")
    subjects = utilities.get_json(req.data)
    return req, subjects


def add_subjects(client, name):
    data = {
        "name": name,
        "description": "description of {}".format(name),
        "password": "password for {}".format(name),
        "email": "{}@moon".format(name)
    }
    req = client.post("/subjects", data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    subjects = utilities.get_json(req.data)
    return req, subjects


def delete_subject(client):
    subjects = get_subjects(client)
    for key, value in subjects[1]['subjects'].items():
        if value['name'] == "testuser":
            req = client.delete("/subjects/{}".format(key))
            break
    return req


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
    req, subjects = add_subjects(client, "testuser")
    assert req.status_code == 200
    value = list(subjects["subjects"].values())[0]
    assert "subjects" in subjects
    assert value['name'] == "testuser"
    assert value["email"] == "{}@moon".format("testuser")


def test_perimeter_add_subject_without_name():
    client = utilities.register_client()
    req, subjects = add_subjects(client, "")
    assert req.status_code == 500
    assert json.loads(req.data)["message"] == "Empty String"


def test_perimeter_add_subject_with_name_contain_spaces():
    client = utilities.register_client()
    req, subjects = add_subjects(client, "test user")
    assert req.status_code == 500
    assert json.loads(req.data)["message"] == "String contains space"


def test_perimeter_delete_subject():
    client = utilities.register_client()
    req = delete_subject(client)
    assert req.status_code == 200


def test_perimeter_delete_subjects_without_perimeter_id():
    client = utilities.register_client()
    req = delete_subjects_without_perimeter_id(client)
    assert req.status_code == 500


def get_objects(client):
    req = client.get("/objects")
    objects = utilities.get_json(req.data)
    return req, objects


def add_objects(client, name):
    data = {
        "name": name,
        "description": "description of {}".format(name),
    }
    req = client.post("/objects", data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    objects = utilities.get_json(req.data)
    return req, objects


def delete_object(client):
    objects = get_objects(client)
    for key, value in objects[1]['objects'].items():
        if value['name'] == "testuser":
            req = client.delete("/objects/{}".format(key))
            break
    return req


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
    assert req.status_code == 200
    value = list(objects["objects"].values())[0]
    assert "objects" in objects
    assert value['name'] == "testuser"


def test_perimeter_add_object_without_name():
    client = utilities.register_client()
    req, objects = add_objects(client, "")
    assert req.status_code == 500
    assert json.loads(req.data)["message"] == "Empty String"


def test_perimeter_add_object_with_name_contain_spaces():
    client = utilities.register_client()
    req, objects = add_objects(client, "test user")
    assert req.status_code == 500
    assert json.loads(req.data)["message"] == "String contains space"


def test_perimeter_delete_object():
    client = utilities.register_client()
    req = delete_object(client)
    assert req.status_code == 200


def test_perimeter_delete_objects_without_perimeter_id():
    client = utilities.register_client()
    req = delete_objects_without_perimeter_id(client)
    assert req.status_code == 500


def get_actions(client):
    req = client.get("/actions")
    actions = utilities.get_json(req.data)
    return req, actions


def add_actions(client, name):
    data = {
        "name": name,
        "description": "description of {}".format(name),
    }
    req = client.post("/actions", data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    actions = utilities.get_json(req.data)
    return req, actions


def delete_actions(client):
    actions = get_actions(client)
    for key, value in actions[1]['actions'].items():
        if value['name'] == "testuser":
            req = client.delete("/actions/{}".format(key))
            break
    return req


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
    assert req.status_code == 200
    value = list(actions["actions"].values())[0]
    assert "actions" in actions
    assert value['name'] == "testuser"


def test_perimeter_add_actions_without_name():
    client = utilities.register_client()
    req, actions = add_actions(client, "")
    assert req.status_code == 500
    assert json.loads(req.data)["message"] == "Empty String"


def test_perimeter_add_actions_with_name_contain_spaces():
    client = utilities.register_client()
    req, actions = add_actions(client, "test user")
    assert req.status_code == 500
    assert json.loads(req.data)["message"] == "String contains space"


def test_perimeter_delete_actions():
    client = utilities.register_client()
    req = delete_actions(client)
    assert req.status_code == 200


def test_perimeter_delete_actions_without_perimeter_id():
    client = utilities.register_client()
    req = delete_actions_without_perimeter_id(client)
    assert req.status_code == 500

