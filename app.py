from flask import Flask
from flask_restful import Api

from exceptions import api_errors
from resources.contact import ContactResource

app = Flask(__name__)
api = Api(app, errors=api_errors)

api.add_resource(ContactResource, '/contact', '/contact/<contact_id>')

if __name__ == '__main__':
    app.run()
