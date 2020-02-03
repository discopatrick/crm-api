from models import Contact


def test_add(client):
    r = client.post('/contact', data=dict(
        username='username', first_name='first', last_name='last'
    ))

    assert r.status_code == 200

    all_contacts = Contact.query.all()
    assert len(all_contacts) == 1
    assert all_contacts[0].username == 'username'
