from uuid import uuid4

from database import db_session
from models import Contact


def unique():
    return str(uuid4())


def test_add(client):
    r = client.post('/contact', data=dict(
        username='username', first_name='first', last_name='last'
    ))

    assert r.status_code == 200

    all_contacts = Contact.query.all()
    assert len(all_contacts) == 1
    assert all_contacts[0].username == 'username'


def test_duplicate_username_returns_409(client):
    name_to_duplicate = unique()
    c = Contact(username=name_to_duplicate, first_name='first', last_name='last')
    db_session.add(c)
    db_session.commit()

    r = client.post('/contact', data=dict(
        username=name_to_duplicate, first_name='first', last_name='last'
    ))

    assert r.status_code == 409
