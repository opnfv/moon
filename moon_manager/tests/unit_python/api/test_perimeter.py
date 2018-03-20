# import moon_manager
# import moon_manager.api
import json
import api.utilities as utilities


def get_subjects(client):
    req = client.get("/subjects")
    assert req.status_code == 200
    subjects = utilities.get_json(req.data)
    assert isinstance(subjects, dict)
    assert "subjects" in subjects
    return subjects


def add_subjects(client, name):
    data = {
        "name": name,
        "description": "description of {}".format(name),
        "password": "password for {}".format(name),
        "email": "{}@moon".format(name)
    }
    req = client.post("/subjects", data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    assert req.status_code == 200
    subjects = utilities.get_json(req.data)
    assert isinstance(subjects, dict)
    print(list(subjects["subjects"].keys()))
    key = list(subjects["subjects"].keys())[0]
    value = list(subjects["subjects"].values())[0]
    assert "subjects" in subjects
    assert key == "1111111111111"
    assert value['id'] == "1111111111111"
    assert value['name'] == name
    assert value["description"] == "description of {}".format(name)
    assert value["email"] == "{}@moon".format(name)
    return subjects


def add_subjects_without_name(client, name):
    data = {
        "name": name,
        "description": "description of {}".format(name),
        "password": "password for {}".format(name),
        "email": "{}@moon".format(name)
    }
    req = client.post("/subjects", data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    assert req.status_code == 500


def delete_subject(client, name):
    subjects = get_subjects(client)
    for key, value in subjects['subjects'].items():
        if value['name'] == name:
            req = client.delete("/subjects/{}".format(key))
            assert req.status_code == 200
            break
    subjects = get_subjects(client)
    assert name not in [x['name'] for x in subjects["subjects"].values()]


def test_subject():
    client = utilities.register_client()
    get_subjects(client)
    add_subjects(client, "testuser")
    add_subjects_without_name(client, "")
    delete_subject(client, "testuser")


def get_objects(client):
    req = client.get("/objects")
    assert req.status_code == 200
    objects = utilities.get_json(req.data)
    assert isinstance(objects, dict)
    assert "objects" in objects
    return objects


def add_objects(client, name):
    data = {
        "name": name,
        "description": "description of {}".format(name),
    }
    req = client.post("/objects", data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    assert req.status_code == 200
    objects = utilities.get_json(req.data)
    assert isinstance(objects, dict)
    key = list(objects["objects"].keys())[0]
    value = list(objects["objects"].values())[0]
    assert "objects" in objects
    assert value['name'] == name
    assert value["description"] == "description of {}".format(name)
    return objects


def delete_objects(client, name):
    objects = get_objects(client)
    for key, value in objects['objects'].items():
        if value['name'] == name:
            req = client.delete("/objects/{}".format(key))
            assert req.status_code == 200
            break
    objects = get_objects(client)
    assert name not in [x['name'] for x in objects["objects"].values()]


def test_objects():
    client = utilities.register_client()
    get_objects(client)
    add_objects(client, "testuser")
    delete_objects(client, "testuser")


def get_actions(client):
    req = client.get("/actions")
    assert req.status_code == 200
    actions = utilities.get_json(req.data)
    assert isinstance(actions, dict)
    assert "actions" in actions
    return actions


def add_actions(client, name):
    data = {
        "name": name,
        "description": "description of {}".format(name),
    }
    req = client.post("/actions", data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})
    assert req.status_code == 200
    actions = utilities.get_json(req.data)
    assert isinstance(actions, dict)
    key = list(actions["actions"].keys())[0]
    value = list(actions["actions"].values())[0]
    assert "actions" in actions
    assert value['name'] == name
    assert value["description"] == "description of {}".format(name)
    return actions


def delete_actions(client, name):
    actions = get_actions(client)
    for key, value in actions['actions'].items():
        if value['name'] == name:
            req = client.delete("/actions/{}".format(key))
            assert req.status_code == 200
            break
    actions = get_actions(client)
    assert name not in [x['name'] for x in actions["actions"].values()]


def test_actions():
    client = utilities.register_client()
    get_actions(client)
    add_actions(client, "testuser")
    delete_actions(client, "testuser")
