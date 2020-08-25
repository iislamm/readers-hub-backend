def test_hello(client):
    res = client.get('hello')
    assert res.data == b'Hello, world'
