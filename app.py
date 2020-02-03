from flask import Flask, request

from database import db_session
from models import Contact

app = Flask(__name__)


@app.route('/contact', methods=('POST',))
def add_contact():
    username = request.form['username']
    first_name = request.form['first_name']
    last_name = request.form['last_name']

    c = Contact(username=username,
                first_name=first_name,
                last_name=last_name)

    db_session.add(c)
    db_session.commit()
    return 'Added contact'


if __name__ == '__main__':
    app.run()
