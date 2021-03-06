from flask import Flask
from flask_restful import Api

from crm.database import db_session
from crm.exceptions import api_errors
from crm.resources.contact import ContactResource

app = Flask(__name__)
api = Api(app, errors=api_errors)

api.add_resource(ContactResource, '/contact', '/contact/<contact_id>')


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    app.run()
