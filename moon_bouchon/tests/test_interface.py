import requests
from uuid import uuid4
import pytest


@pytest.fixture
def args():
    return {
        "project_id": uuid4().hex,
        "subject_id": uuid4().hex,
        "object_id": uuid4().hex,
        "action_id": uuid4().hex
    }


def test_false(args):
    url = "http://127.0.0.1:31002/interface/authz/deny/{project_id}" \
          "/{subject_id}/{object_id}/{action_id}".format(**args)
    data = {'rule': 'start',
            'target': '{"target": {"name": "vm0"}, "user_id": "user0"}',
            'credentials': 'null'}
    req = requests.get(
        url, json=data,
        headers={'content-type': "application/x-www-form-urlencode"}
    )
    assert req.status_code == 200
    assert "result" in req.json()
    assert req.json()["result"] == False


def test_true(args):
    url = "http://127.0.0.1:31002/interface/authz/grant/{project_id}" \
          "/{subject_id}/{object_id}/{action_id}".format(**args)

    data = {'rule': 'start',
            'target': '{"target": {"name": "vm0"}, "user_id": "user0"}',
            'credentials': 'null'}
    req = requests.get(
        url, json=data,
        headers={'content-type': "application/x-www-form-urlencode"}
    )
    assert req.status_code == 200
    assert "result" in req.json()
    assert req.json()["result"] == True


def test_random(args):
    url = "http://127.0.0.1:31002/interface/authz/{project_id}" \
          "/{subject_id}/{object_id}/{action_id}".format(**args)

    data = {'rule': 'start',
            'target': '{"target": {"name": "vm0"}, "user_id": "user0"}',
            'credentials': 'null'}
    req = requests.get(
        url, json=data,
        headers={'content-type': "application/x-www-form-urlencode"}
    )
    assert req.status_code == 200
    assert "result" in req.json()
    assert req.json()["result"] in (False, True)

