import os
import json
from urllib.request import urlopen

from authlib.oauth2.rfc7523 import JWTBearerTokenValidator
from authlib.jose.rfc7517.jwk import JsonWebKey
from dotenv import load_dotenv
from authlib.integrations.flask_oauth2 import ResourceProtector


class Auth0JWTBearerTokenValidator(JWTBearerTokenValidator):
    def __init__(self: "Auth0JWTBearerTokenValidator", domain: str, audience: str, dev_public_key: str | None | dict=None):
        """
        Initialize the Auth0 JWT Bearer Token Validator.

        Args:
            domain (str): The Auth0 domain.
            audience (str): The audience for the token.
            dev_public_key (str | None | dict): The public key to use for token validation.
        """
        issuer = f"https://{domain}/"
        if dev_public_key:
            if isinstance(dev_public_key, str):
                dev_public_key = json.loads(dev_public_key)
            public_key = JsonWebKey.import_key_set(dev_public_key)
        else:
            jsonurl = urlopen(f"{issuer}.well-known/jwks.json")
            public_key = JsonWebKey.import_key_set(
                json.loads(jsonurl.read())
            )
        super(Auth0JWTBearerTokenValidator, self).__init__(
            public_key
        )
        # SPS: required claims for the token
        self.claims_options = {
            "exp": {"essential": True},
            "aud": {"essential": True, "value": audience},
            "iss": {"essential": True, "value": issuer},
        }

load_dotenv()
require_auth = ResourceProtector()
default_validator = Auth0JWTBearerTokenValidator(
    os.getenv("AUTH0_DOMAIN"),
    os.getenv("AUTH0_AUDIENCE"),
)

def register_token_validator(validator: Auth0JWTBearerTokenValidator=default_validator) -> None:
    require_auth.register_token_validator(validator)

def getResourceProtector() -> ResourceProtector:
    return require_auth