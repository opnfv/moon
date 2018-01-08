import json


def get_json(data):
    return json.loads(data.decode("utf-8"))

'''
    test case failed to run, and it related to some how
    - import, urls, mocked data 'pipeline'
'''
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
    req = client.post("/authz", data=json.dumps(authz_data))
    assert req.status_code == 200
    assert req.data
    assert isinstance(req.data, bytes)
    assert req.data == b"True"

