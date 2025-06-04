from api.ping import get_pong

def test_get_pong():
    assert get_pong() == "pong"