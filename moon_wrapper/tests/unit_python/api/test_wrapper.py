# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import json


def get_json(data):
    return json.loads(data.decode("utf-8"))


def test_authz_true(context):
    import moon_wrapper.server
    server = moon_wrapper.server.main()
    client = server.app.test_client()
    _target = {
        'target': {
            "name": context.get('object_name'),
        },
        "project_id": context.get('project_id'),
        "user_id": context.get('subject_name')
    }
    authz_data = {
        'rule': context.get('action_name'),
        'target': json.dumps(_target),
        'credentials': 'null'}
    req = client.post("/authz/oslo", data=json.dumps(authz_data))
    assert req.status_code is 200
    assert req.data
    assert isinstance(req.data, bytes)
    assert req.data == b"True"

def test_authz_error_response_code(context):
    import moon_wrapper.server
    server = moon_wrapper.server.main()
    client = server.app.test_client()
    _target = {
        'target': {
            "name": context.get('object_name'),
        },
        "project_id": context.get('invalid_project_id'),
        "user_id": context.get('subject_name')
    }
    authz_data = {
        'rule': context.get('action_name'),
        'target': json.dumps(_target),
        'credentials': 'null'}
    req = client.post("/authz/oslo", data=json.dumps(authz_data))
    assert req.status_code is 200
    assert req.data
    assert isinstance(req.data, bytes)
    assert req.data == b"False"

def test_authz_error_no_interface_key(context):
    import moon_wrapper.server
    server = moon_wrapper.server.main()
    client = server.app.test_client()
    _target = {
        'target': {
            "name": context.get('object_name'),
        },
        "project_id": context.get('project_with_no_interface_key'),
        "user_id": context.get('subject_name')
    }
    authz_data = {
        'rule': context.get('action_name'),
        'target': json.dumps(_target),
        'credentials': 'null'}
    req = client.post("/authz/oslo", data=json.dumps(authz_data))

    assert req.data == b"False"