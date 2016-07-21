def test_login(client):
    resp = client.get('/tests/test_abort?code=401')
    assert 401 == resp.status_code
