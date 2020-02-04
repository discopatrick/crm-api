from datetime import datetime, timedelta
from uuid import uuid4

from celery import Celery

from crm.database import db_session
from crm.models import Contact, Email

app = Celery('tasks', broker='redis://localhost')


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(15.0, create_contact.s(), name='Add Contact every 15 seconds')
    sender.add_periodic_task(5.0,
                             delete_contacts_older_than_1_minute.s(),
                             name='Delete Contacts older than 1 minute every 5 seconds')


def get_unique_string():
    return str(uuid4())


@app.task
def create_contact():
    c = Contact(username=get_unique_string(), first_name='first', last_name='last')
    e = Email(email_address=f'{c.username}@localhost')
    e2 = Email(email_address=f'{c.username}@localhost2')
    c.emails = [e, e2]
    db_session.add(c)
    db_session.commit()


@app.task
def delete_contacts_older_than_1_minute():
    q = db_session.query(Contact).filter(Contact.created_at < datetime.now() - timedelta(minutes=1))
    # We cannot simply chain `.delete()` onto the previous line, as that would bypass
    # the cascade deletion of the related Email objects. Looping through, as below,
    # will ensure cascade deletion.
    for contact in q:
        db_session.delete(contact)
    db_session.commit()
