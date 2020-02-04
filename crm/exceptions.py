class ContactUsernameAlreadyExistsException(Exception):
    pass


api_errors = {
    'ContactUsernameAlreadyExistsException': {
        'message': 'A Contact with that username already exists.',
        'status': 409,
    },
}
