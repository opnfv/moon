import json
from mock_pods import patch_k8s
from utilities import get_json


def test_get_slaves(context, monkeypatch):
    patch_k8s(monkeypatch)

    import moon_orchestrator.server
    server = moon_orchestrator.server.create_server()
    _client = server.app.test_client()
    req = _client.get("/slaves")
    assert req.status_code == 200
    assert req.data
    data = get_json(req.data)
    assert isinstance(data, dict)
    assert "slaves" in data
