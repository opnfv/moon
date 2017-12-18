import json
from mock_pods import patch_k8s
from utilities import get_json


def test_get_pods(context, monkeypatch):
    patch_k8s(monkeypatch)

    import moon_orchestrator.server
    server = moon_orchestrator.server.main()
    _client = server.app.test_client()
    req = _client.get("/pods")
    assert req.status_code == 200
    assert req.data
    data = get_json(req.data)
    assert isinstance(data, dict)
    assert "pods" in data


def test_add_pods(context, monkeypatch):
    patch_k8s(monkeypatch)

    import moon_orchestrator.server
    server = moon_orchestrator.server.main()
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


def test_delete_pods(context, monkeypatch):
    # TODO
    pass
