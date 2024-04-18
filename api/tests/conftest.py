import os
import pytest

from .. import create_app
from ..db.db_utils import init_db, clean_db


@pytest.fixture
def app():
    app = create_app({
        "TESTING":True, 
        "DATABASE":os.path.join(os.curdir, 'test_db.sqlite'),
        "JWT_PUBLIC_KEY": "tests/test_keys/jwtRS256.key.pub",
        "AUTH0_DOMAIN": "test_domain",
        "AUTH0_AUDIENCE": "test_audience"
        })
    with app.app_context():
        init_db()
    yield app



@pytest.fixture(autouse=True)
def reset_db(app):
    with app.app_context():
        clean_db()
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

