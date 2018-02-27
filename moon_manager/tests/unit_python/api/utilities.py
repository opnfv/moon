import json


def get_json(data):
    return json.loads(data.decode("utf-8"))


def register_client():
    import moon_manager.server
    server = moon_manager.server.create_server()
    client = server.app.test_client()
    return client


def get_policy_id():
    import api.test_policies as policies
    client = register_client()
    policy_id = ''
    req, policy = policies.get_policies(client)
    for id in policy['policies']:
        if id:
            policy_id = id
            break
    print("policy id {}".format(policy_id))
    if not policy_id:
        policies.add_policies(client, "testuser")
        policy_id = get_policy_id()
    return policy_id
