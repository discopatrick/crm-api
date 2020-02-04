from flask_restful import fields, reqparse, Resource, marshal_with, abort

from database import db_session
from exceptions import ContactUsernameAlreadyExistsException
from models import Contact, Email

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
contact_post_parser.add_argument(
    'email', dest='email',
    location='form', required=False,
    # Not required; contacts may be posted without email addresses
    help="The contact's email addresses: {error_msg}",
    action='append',
    # append, because there could be multiple 'email' args
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

contact_get_parser = reqparse.RequestParser()
contact_get_parser.add_argument(
    'username', dest='username',
    location='args', required=False,
    help="The contact's username: {error_msg}",
    store_missing=False,
)


class ContactResource(Resource):
    @marshal_with(contact_fields)
    def post(self):
        kwargs = contact_post_parser.parse_args()
        if 'email' in kwargs:
            addresses = kwargs.pop('email')

        contact = Contact(**kwargs)
        db_session.add(contact)
        try:
            db_session.commit()
        # Should really catch sqlite.IntegrityError here but
        # doing so skips the except block...
        except Exception:
            db_session.rollback()
            raise ContactUsernameAlreadyExistsException

        if addresses:
            for address in addresses:
                contact.emails.append(Email(email_address=address))
            db_session.add(contact)
            db_session.commit()

        return contact

    @marshal_with(contact_fields)
    def patch(self, contact_id):
        kwargs = contact_patch_parser.parse_args()

        db_session.query(Contact).filter_by(id=contact_id).update(kwargs)
        db_session.commit()

        contact = Contact.query.get(contact_id)
        return contact

    def delete(self, contact_id):
        db_session.query(Contact).filter_by(id=contact_id).delete()
        db_session.commit()

        return {'message': f'Contact with id {contact_id} deleted.'}

    @marshal_with(contact_fields)
    def get(self):
        kwargs = contact_get_parser.parse_args()
        if 'username' in kwargs:
            username = kwargs['username']
            c = Contact.query.filter_by(username=username).one_or_none()
            if not c:
                abort(404, message=f"Contact {username} doesn't exist")
            return c
        else:
            return Contact.query.all()
