import json
from uuid import uuid4

def get_json(data):
    return json.loads(data.decode("utf-8"))


def register_client():
    import moon_manager.server
    server = moon_manager.server.create_server()
    client = server.app.test_client()
    return client


def get_policy_id():
    from helpers import policy_helper
    value = {
        "name": "test_policy"+uuid4().hex,
        "model_id": "",
        "genre": "authz",
        "description": "test",
        }
    policy_helper.add_policies(value=value)
    req = policy_helper.get_policies()
    policy_id = list(req.keys())[0]
    return policy_id
