import requests


def test_false():
    url = "http://127.0.0.1:31002/wrapper/authz/deny"

    data = {'rule': 'start', 'target': '{"target": {"name": "vm0"}, "user_id": "user0"}', 'credentials': 'null'}
    req = requests.post(
        url, json=data,
        headers={'content-type': "application/x-www-form-urlencode"}
    )
    assert req.status_code == 200
    assert req.text == "False"


def test_true():
    url = "http://127.0.0.1:31002/wrapper/authz/grant"

    data = {'rule': 'start', 'target': '{"target": {"name": "vm0"}, "user_id": "user0"}', 'credentials': 'null'}
    req = requests.post(
        url, json=data,
        headers={'content-type': "application/x-www-form-urlencode"}
    )
    assert req.status_code == 200
    assert req.text == "True"


def test_random():
    url = "http://127.0.0.1:31002/wrapper/authz"

    data = {'rule': 'start', 'target': '{"target": {"name": "vm0"}, "user_id": "user0"}', 'credentials': 'null'}
    req = requests.post(
        url, json=data,
        headers={'content-type': "application/x-www-form-urlencode"}
    )
    assert req.status_code == 200
    assert req.text in ("False", "True")

