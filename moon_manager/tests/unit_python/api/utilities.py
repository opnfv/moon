import json


def get_json(data):
    return json.loads(data.decode("utf-8"))


def register_client():
    import moon_manager.server
    server = moon_manager.server.main()
    client = server.app.test_client()
    return client