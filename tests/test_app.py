from uuid import uuid4

from werkzeug.datastructures import MultiDict

from database import db_session
from models import Contact, Email


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


def test_add_with_emails(client):
    # We need to post duplicate keys for 'email'
    # (just as a web form or any other HTTP POST might do),
    # thus we need a MultiDict.
    # TODO: make endpoints accept JSON payloads instead?
    # (Then we could post multiples as lists)

    data = MultiDict()
    data.add('username', 'new_contact_with_emails')
    data.add('first_name', 'New Contact')
    data.add('last_name', 'With Emails')

    email1 = f'{unique()}@localhost'
    email2 = f'{unique()}@localhost'

    # add two emails
    data.add('email', email1)
    data.add('email', email2)

    r = client.post('/contact', data=data)
    assert r.status_code == 200

    all_contacts = Contact.query.all()
    assert len(all_contacts) == 1

    c = Contact.query.first()
    assert len(c.emails) == 2
    assert c.emails[0].email_address == email1
    assert c.emails[1].email_address == email2


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


def test_delete(client):
    c = Contact(username='to delete', first_name='To', last_name='Delete')
    db_session.add(c)
    db_session.commit()

    # `c` should be a deleted object by the end of this test,
    # so grab hold of the id here:
    contact_id = c.id

    r = client.delete(f'/contact/{contact_id}')
    assert r.status_code == 200

    q = Contact.query.filter_by(id=contact_id)
    assert q.count() == 0


def test_list(client):
    for username in ('one', 'two', 'three'):
        c = Contact(username=username, first_name=username, last_name=username)
        db_session.add(c)
    db_session.commit()

    r = client.get('/contact')

    assert r.status_code == 200
    assert len(r.json) == 3


def test_list_with_emails(client):
    for username in ('one', 'two', 'three'):
        c = Contact(username=username, first_name=username, last_name=username)
        e = Email(email_address=f'{username}@localhost')
        c.emails.append(e)
        db_session.add(c)
    db_session.commit()

    r = client.get('/contact')

    assert r.status_code == 200
    assert len(r.json) == 3
    assert len(r.json[0]['emails']) == 1


def test_find(client):
    username_to_find = unique()
    c = Contact(username=username_to_find, first_name='first', last_name='last')
    db_session.add(c)
    db_session.commit()

    r = client.get(f'/contact?username={username_to_find}')

    assert r.status_code == 200
    assert r.json.get('username') == username_to_find


def test_find_non_existent_returns_404(client):
    non_existent_username = unique()

    r = client.get(f'/contact?username={non_existent_username}')

    assert r.status_code == 404
