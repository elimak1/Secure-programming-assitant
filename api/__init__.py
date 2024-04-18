import os

from flask import Flask, jsonify
from flask_cors import CORS
from .core import limiter
from .authenticate import register_token_validator, Auth0JWTBearerTokenValidator
from .tests.token_utils import pubkey_to_jwks

def create_app(test_config=None) -> Flask:
    
    app = Flask(__name__, instance_relative_config=True)
    limiter.init_app(app)

    CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})



    if test_config:
        app.config.update(test_config)
    else:
            app.config.from_mapping(
                {"DATABASE": os.path.join(app.instance_path, "flaskr.sqlite")},
            )
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    register_error_handler(app)

    if test_config and 'JWT_PUBLIC_KEY' in test_config:
        # Set up with custom test validator
        public_key = pubkey_to_jwks(test_config['JWT_PUBLIC_KEY'])
        validator = Auth0JWTBearerTokenValidator(
            test_config.get('AUTH0_DOMAIN', 'test_domain'),
            test_config.get('AUTH0_AUDIENCE', 'test_audience'),
            public_key
        )
        register_token_validator(validator)
    else:
        # Default production setup
        register_token_validator()
    
    from api.db import db_utils
    db_utils.init_app(app)

    from api import llm
    app.register_blueprint(llm.bp)

    return app

def register_error_handler(app):
    def ratelimit_handler(e):
        return jsonify(error=429, message=str(e.description)), 429
    
    def not_found(e):
        return jsonify(error=404, message=str(e.description)), 404
    
    def internal_server_error(e):
        return jsonify(error=500, message=str(e.description)), 500
    
    app.register_error_handler(429, ratelimit_handler)
    app.register_error_handler(404, not_found)
    app.register_error_handler(500, internal_server_error)
    return app