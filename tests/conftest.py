import pytest

from crm import app as flask_app
from crm.database import init_db, empty_db


@pytest.fixture
def app():

    with flask_app.app_context():
        init_db()

    yield flask_app

    with flask_app.app_context():
        empty_db()


@pytest.fixture
def client(app):
    return app.test_client()
