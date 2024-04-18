import os
import pytest

from .. import create_app
from ..authenticate import getResourceProtector, Auth0JWTBearerTokenValidator
from .token_utils import pubkey_to_jwks


@pytest.fixture
def app():
    app = create_app({
        "TESTING":True, 
        "DATABASE":os.path.join(os.curdir, 'test_db.sqlite'),
        "JWT_PUBLIC_KEY": "tests/test_keys/jwtRS256.key.pub",
        "AUTH0_DOMAIN": "test_domain",
        "AUTH0_AUDIENCE": "test_audience"
        })
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()
