from types import SimpleNamespace
from api.ping import handler

def test_ping_handler_returns_pong():
    request = SimpleNamespace(args={})
    response = SimpleNamespace(status_code=None, headers={}, body=None)

    result = handler(request, response)

    assert result.status_code == 200
    assert result.body == "pong"
