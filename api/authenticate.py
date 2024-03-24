import os
import json
from urllib.request import urlopen

from authlib.oauth2.rfc7523 import JWTBearerTokenValidator
from authlib.jose.rfc7517.jwk import JsonWebKey
from dotenv import load_dotenv
from authlib.integrations.flask_oauth2 import ResourceProtector


class Auth0JWTBearerTokenValidator(JWTBearerTokenValidator):
    def __init__(self, domain, audience):
        issuer = f"https://{domain}/"
        jsonurl = urlopen(f"{issuer}.well-known/jwks.json")
        public_key = JsonWebKey.import_key_set(
            json.loads(jsonurl.read())
        )
        super(Auth0JWTBearerTokenValidator, self).__init__(
            public_key
        )
        self.claims_options = {
            "exp": {"essential": True},
            "aud": {"essential": True, "value": audience},
            "iss": {"essential": True, "value": issuer},
        }

load_dotenv()
require_auth = ResourceProtector()
validator = Auth0JWTBearerTokenValidator(
    os.getenv("AUTH0_DOMAIN"),
    os.getenv("AUTH0_AUDIENCE")
)
require_auth.register_token_validator(validator)


def getResourceProtector():
    return require_auth

