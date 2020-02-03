from flask_restful import fields, reqparse, Resource, marshal_with

from database import db_session
from models import Contact

contact_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
}

contact_post_parser = reqparse.RequestParser()
contact_post_parser.add_argument(
    'username', dest='username',
    location='form', required=True,
    help="The contact's username: {error_msg}"
)
contact_post_parser.add_argument(
    'first_name', dest='first_name',
    location='form', required=True,
    help="The contact's first name: {error_msg}"
)
contact_post_parser.add_argument(
    'last_name', dest='last_name',
    location='form', required=True,
    help="The contact's last name: {error_msg}"
)


class ContactResource(Resource):
    @marshal_with(contact_fields)
    def post(self):
        kwargs = contact_post_parser.parse_args()
        contact = Contact(**kwargs)
        db_session.add(contact)
        db_session.commit()
        return contact
