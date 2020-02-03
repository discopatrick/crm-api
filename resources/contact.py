from flask_restful import fields, reqparse, Resource, marshal_with

from database import db_session
from exceptions import ContactUsernameAlreadyExistsException
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

contact_patch_parser = reqparse.RequestParser()
contact_patch_parser.add_argument(
    'username', dest='username',
    location='form', required=False,
    help="The contact's username: {error_msg}",
    store_missing=False,
)
contact_patch_parser.add_argument(
    'first_name', dest='first_name',
    location='form', required=False,
    help="The contact's first name: {error_msg}",
    store_missing=False,
)
contact_patch_parser.add_argument(
    'last_name', dest='last_name',
    location='form', required=False,
    help="The contact's last name: {error_msg}",
    store_missing=False,
)


class ContactResource(Resource):
    @marshal_with(contact_fields)
    def post(self):
        kwargs = contact_post_parser.parse_args()
        contact = Contact(**kwargs)
        db_session.add(contact)
        try:
            db_session.commit()
        # Should really catch sqlite.IntegrityError here but
        # doing so skips the except block...
        except Exception:
            db_session.rollback()
            raise ContactUsernameAlreadyExistsException

        return contact

    @marshal_with(contact_fields)
    def patch(self, contact_id):
        kwargs = contact_patch_parser.parse_args()

        db_session.query(Contact).filter_by(id=contact_id).update(kwargs)
        db_session.commit()

        contact = Contact.query.get(contact_id)
        return contact
