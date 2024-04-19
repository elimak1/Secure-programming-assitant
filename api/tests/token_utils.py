import jwt
from datetime import datetime, timedelta, UTC

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import base64
import json
import os

def create_test_token(sub="test_user_id"):
    with open("tests/test_keys/jwtRS256.key", "r") as key_file:
        private_key = key_file.read()
    expires_delta=timedelta(minutes=60)
    AUTH_NAMESPACE = os.getenv("AUTH_NAMESPACE")
    payload = {
        "iss": "https://test_domain/",
        "aud": "test_audience",
        "exp": datetime.now(UTC) + expires_delta,
        "sub": sub, 
        "iat":  datetime.now(UTC),
        f"{AUTH_NAMESPACE}/roles": []
    }
    headers = {
        "alg": "RS256",
        "kid": "test_key_id"
    }
    token = jwt.encode(payload, private_key, algorithm="RS256", headers=headers)
    return token

def pubkey_to_jwks(pubkey_path):
    with open(pubkey_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )

    numbers = public_key.public_numbers()
    exponent = numbers.e
    modulus = numbers.n

    jwk = {
        "kty": "RSA",
        "use": "sig",
        "alg": "RS256",
        "e": base64.urlsafe_b64encode(exponent.to_bytes((exponent.bit_length() + 7) // 8, 'big')).rstrip(b'=').decode('utf-8'),
        "n": base64.urlsafe_b64encode(modulus.to_bytes((modulus.bit_length() + 7) // 8, 'big')).rstrip(b'=').decode('utf-8'),
        "kid": "test_key_id"
    }
    return json.dumps({"keys": [jwk]}, indent=2)