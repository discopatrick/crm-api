def test_add(client):
    r = client.post('/contact', data=dict(
        username='username', first_name='first', last_name='last'
    ))

    assert r.status_code == 200
