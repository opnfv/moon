# import moon_manager
# import moon_manager.api
import json


def get_json(data):
    return json.loads(data.decode("utf-8"))


def get_subjects(client):
    req = client.get("/subjects")
    assert req.status_code == 200
    subjects = get_json(req.data)
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
    subjects = get_json(req.data)
    assert isinstance(subjects, dict)
    key = list(subjects["subjects"].keys())[0]
    value = list(subjects["subjects"].values())[0]
    assert "subjects" in subjects
    assert key == "1111111111111"
    assert value['id'] == "1111111111111"
    assert value['name'] == name
    assert value["description"] == "description of {}".format(name)
    assert value["email"] == "{}@moon".format(name)
    return subjects


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
    import moon_manager.server
    server = moon_manager.server.main()
    client = server.app.test_client()
    get_subjects(client)
    add_subjects(client, "testuser")
    delete_subject(client, "testuser")
