import json
from mock_pods import patch_k8s
from utilities import get_json


def test_get_pods(context, monkeypatch):
    patch_k8s(monkeypatch)

    import moon_orchestrator.server
    server = moon_orchestrator.server.create_server()
    _client = server.app.test_client()
    req = _client.get("/pods")
    assert req.status_code == 200
    assert req.data
    data = get_json(req.data)
    assert isinstance(data, dict)
    assert "pods" in data


def test_get_pods_failure(context, monkeypatch):
    patch_k8s(monkeypatch)

    import moon_orchestrator.server
    server = moon_orchestrator.server.create_server()
    _client = server.app.test_client()
    req = _client.get("/pods/invalid")
    assert req.status_code == 200
    assert req.data
    data = get_json(req.data)
    assert isinstance(data, dict)
    assert not data["pods"]


def test_add_pods_with_pipeline(context, monkeypatch):
    patch_k8s(monkeypatch)

    import moon_orchestrator.server
    server = moon_orchestrator.server.create_server()
    _client = server.app.test_client()
    data = {
        "keystone_project_id": context.get('project_id'),
        "pdp_id": context.get('pdp_id'),
        "security_pipeline": context.get('security_pipeline'),
    }
    req = _client.post("/pods", data=json.dumps(data),
                       headers={'Content-Type': 'application/json'})
    assert req.status_code == 200
    assert req.data
    data = get_json(req.data)
    assert isinstance(data, dict)
    assert "pods" in data
    assert data["pods"]


def test_add_pods_without_pipeline_with_bad_slave_name(context, monkeypatch):
    patch_k8s(monkeypatch)

    import moon_orchestrator.server
    server = moon_orchestrator.server.create_server()
    _client = server.app.test_client()
    data = {
        "slave_name": "test",
    }
    req = _client.post("/pods", data=json.dumps(data),
                       headers={'Content-Type': 'application/json'})
    assert req.status_code == 400
    assert req.data
    data = get_json(req.data)
    assert isinstance(data, dict)
    assert 'The slave is unknown.' in data['message']


def test_add_pods_without_pipeline_with_good_slave_name(context, monkeypatch):
    patch_k8s(monkeypatch)

    import moon_orchestrator.server
    server = moon_orchestrator.server.create_server()
    _client = server.app.test_client()
    data = {
        "slave_name": "active_context",
    }
    req = _client.post("/pods", data=json.dumps(data),
                       headers={'Content-Type': 'application/json'})
    assert req.status_code == 200
    assert req.data
    data = get_json(req.data)
    assert isinstance(data, dict)
    assert "pods" in data
    assert data["pods"]


def test_add_pods_without_pipeline_without_slave_name(context, monkeypatch):
    patch_k8s(monkeypatch)

    import moon_orchestrator.server
    server = moon_orchestrator.server.create_server()
    _client = server.app.test_client()
    data = {
    }
    req = _client.post("/pods", data=json.dumps(data),
                       headers={'Content-Type': 'application/json'})
    assert req.status_code == 400
    assert req.data
    data = get_json(req.data)
    assert isinstance(data, dict)
    assert 'The slave is unknown.' in data['message']


def test_add_pods_with_no_data(context, monkeypatch):
    patch_k8s(monkeypatch)
    import moon_orchestrator.server
    server = moon_orchestrator.server.create_server()
    _client = server.app.test_client()
    req = _client.post("/pods", data=json.dumps({}),
                       headers={'Content-Type': 'application/json'})
    assert req.status_code == 400
    assert req.data
    data = get_json(req.data)
    assert 'The slave is unknown.' in data['message']


def test_add_pods_with_no_policies_no_models(context, monkeypatch, no_requests):
    patch_k8s(monkeypatch)

    import moon_orchestrator.server
    server = moon_orchestrator.server.create_server()
    _client = server.app.test_client()
    no_requests.get("http://manager:8082/policies",
                    json={'policies': {}})

    no_requests.get("http://manager:8082/models",
                    json={'models': {}})
    data = {
        "keystone_project_id": context.get('project_id'),
        "pdp_id": context.get('pdp_id'),
        "security_pipeline": context.get('security_pipeline'),
    }
    req = _client.post("/pods", data=json.dumps(data),
                       headers={'Content-Type': 'application/json'})
    assert req.status_code == 200


def test_delete_pods(context, monkeypatch):
    # TODO
    pass
