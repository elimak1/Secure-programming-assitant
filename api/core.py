from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from api.authenticate import getResourceProtector
import os

require_auth = getResourceProtector()

limiter = Limiter(key_func=get_remote_address)

AUTH_NAMESPACE = os.getenv("AUTH_NAMESPACE")

assert AUTH_NAMESPACE, "AUTH_NAMESPACE not set"

def get_prompt_limit_from_config():
    token = require_auth.acquire_token()
    roles = token.get(f"{AUTH_NAMESPACE}/roles")
    if "admin" in roles:
        return '' # No limit for admins
    return '50/hour;100/day'
