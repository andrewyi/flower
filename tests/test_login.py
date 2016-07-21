def test_login(client):
    resp = client.get('/orders/order_list')
    assert 302 == resp.status_code
