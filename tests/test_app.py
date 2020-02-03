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


def test_update(client):
    name_to_update_to = unique()
    first_name = unique()
    last_name = unique()

    c = Contact(username='original_username', first_name=first_name, last_name=last_name)
    db_session.add(c)
    db_session.commit()

    contact_id = c.id

    r = client.patch(f'/contact/{contact_id}', data=dict(
        username=name_to_update_to
    ))
    assert r.status_code == 200

    # We need to clear the db session and reload the object
    # from the db if we truly want to test that the object
    # has been saved to the db with the new values.
    db_session.expunge_all()

    c = Contact.query.get(contact_id)
    assert c.username == name_to_update_to

    # Assert that the other fields are still their original values
    assert c.first_name == first_name
    assert c.last_name == last_name
