import json
import conftest


def get_json(data):
    return json.loads(data.decode("utf-8"))


def test_authz_true(context):

    import moon_interface.server
    server = moon_interface.server.create_server()
    client = server.app.test_client()
    req = client.get("/authz/{p_id}/{s_id}/{o_id}/{a_id}".format(
        p_id=context["pdp_id"],
        s_id=context["subject_name"],
        o_id=context["object_name"],
        a_id=context["action_name"],
    ))
    assert req.status_code == 200
    data = get_json(req.data)
    assert data
    assert "result" in data
    assert data['result'] is True


def test_authz_false(context):
    import moon_interface.server
    server = moon_interface.server.create_server()
    client = server.app.test_client()

    req = client.get("/authz/{p_id}/{s_id}/{o_id}/{a_id}".format(
        p_id=None,
        s_id=context["subject_name"],
        o_id=context["object_name"],
        a_id=context["action_name"],
    ))
    assert req.status_code == 403
    data = get_json(req.data)
    assert data
    assert "result" in data
    assert data['result'] is False


def test_authz_effect_unset(context, set_consul_and_db):
    import moon_interface.server
    server = moon_interface.server.create_server()
    client = server.app.test_client()

    set_consul_and_db.register_uri(
        'POST', 'http://127.0.0.1:8081/authz',
        content=conftest.get_pickled_context_invalid()
    )

    req = client.get("/authz/{p_id}/{s_id}/{o_id}/{a_id}".format(
        p_id=context["pdp_id"],
        s_id=context["subject_name"],
        o_id=context["object_name"],
        a_id=context["action_name"],
    ))
    assert req.status_code == 401
    data = get_json(req.data)
    assert data
    assert "result" in data
    assert data['result'] is False


def test_authz_invalid_ip(context, set_consul_and_db):
    import moon_interface.server
    server = moon_interface.server.create_server()
    client = server.app.test_client()

    set_consul_and_db.register_uri(
        'POST', 'http://127.0.0.1:8081/authz', status_code=500
    )

    req = client.get("/authz/{p_id}/{s_id}/{o_id}/{a_id}".format(
        p_id=context["pdp_id"],
        s_id=context["subject_name"],
        o_id=context["object_name"],
        a_id=context["action_name"],
    ))
    assert req.status_code == 403
