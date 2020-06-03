import json
import pickle
import pytest


def get_data(data):
    return pickle.loads(data)


def get_json(data):
    return json.loads(data.decode("utf-8"))


def run(component_data, cache, context):
    from moon_authz.api.authorization import Authz
    authz = Authz(component_data=component_data, cache=cache)
    authz.context = context
    authz.run()


def test_authz_true(context):
    import moon_authz.server
    from python_moonutilities.context import Context
    from python_moonutilities.cache import Cache
    server = moon_authz.server.create_server()
    client = server.app.test_client()
    CACHE = Cache()
    CACHE.update()
    print(CACHE.pdp)
    _context = Context(context, CACHE)
    req = client.post("/authz", data=pickle.dumps(_context))
    assert req.status_code == 200
    data = get_data(req.data)
    assert data
    assert isinstance(data, Context)
    policy_id = data.headers[0]
    assert policy_id
    assert "effect" in data.pdp_set[policy_id]
    assert data.pdp_set[policy_id]['effect'] == "grant"


def test_user_not_allowed(context):
    import moon_authz.server
    from python_moonutilities.context import Context
    from python_moonutilities.cache import Cache
    server = moon_authz.server.create_server()
    client = server.app.test_client()
    CACHE = Cache()
    CACHE.update()
    context['subject_name'] = "user_not_allowed"
    _context = Context(context, CACHE)
    req = client.post("/authz", data=pickle.dumps(_context))
    assert req.status_code == 400
    data = get_json(req.data)
    assert data
    assert isinstance(data, dict)
    assert "message" in data
    assert data["message"] == "Cannot find subject user_not_allowed"


def test_object_not_allowed(context):
    import moon_authz.server
    from python_moonutilities.context import Context
    from python_moonutilities.cache import Cache
    server = moon_authz.server.create_server()
    client = server.app.test_client()
    CACHE = Cache()
    CACHE.update()
    context['subject_name'] = "testuser"
    context['object_name'] = "invalid"
    _context = Context(context, CACHE)
    req = client.post("/authz", data=pickle.dumps(_context))
    assert req.status_code == 400
    data = get_json(req.data)
    assert data
    assert isinstance(data, dict)
    assert "message" in data
    assert data["message"] == "Cannot find object invalid"


def test_action_not_allowed(context):
    import moon_authz.server
    from python_moonutilities.context import Context
    from python_moonutilities.cache import Cache
    server = moon_authz.server.create_server()
    client = server.app.test_client()
    CACHE = Cache()
    CACHE.update()
    context['subject_name'] = "testuser"
    context['object_name'] = "vm1"
    context['action_name'] = "invalid"
    _context = Context(context, CACHE)
    req = client.post("/authz", data=pickle.dumps(_context))
    assert req.status_code == 400
    data = get_json(req.data)
    assert data
    assert isinstance(data, dict)
    assert "message" in data
    assert data["message"] == "Cannot find action invalid"


def test_authz_with_empty_pdp_set(context):
    from python_moonutilities.context import Context
    from python_moonutilities.cache import Cache
    CACHE = Cache()
    CACHE.update()
    _context = Context(context, CACHE)
    component_data = {
        'component_id': 'component_id1',
        'pdp_id': 'pdp_id1',
        'meta_rule_id': 'meta_rule_id1',
        'keystone_project_id': 'keystone_project_id1',
    }
    with pytest.raises(Exception) as exception_info:
        run(component_data, CACHE, _context)
    assert str(exception_info.value) == '400: Pdp Unknown'
