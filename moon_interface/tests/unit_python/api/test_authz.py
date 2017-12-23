import json


def get_json(data):
    return json.loads(data.decode("utf-8"))


def test_authz_true(context):
    import moon_interface.server
    server = moon_interface.server.main()
    client = server.app.test_client()
    req = client.get("/authz/{p_id}/{s_id}/{o_id}/{a_id}".format(
        p_id=context["project_id"],
        s_id=context["subject_name"],
        o_id=context["object_name"],
        a_id=context["action_name"],
    ))
    assert req.status_code == 200
    data = get_json(req.data)
    assert data
    assert "result" in data
    assert data['result'] == True

