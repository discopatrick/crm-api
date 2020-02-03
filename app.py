from flask import Flask
from flask_restful import Api

from resources.contact import ContactResource

app = Flask(__name__)
api = Api(app)

api.add_resource(ContactResource, '/contact')

if __name__ == '__main__':
    app.run()
