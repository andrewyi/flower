def test_login(client):
    resp = client.get('/tests/test_abort?code=404')
    assert 404 == resp.status_code
