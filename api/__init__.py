import os

from flask import Flask, jsonify
from flask_cors import CORS
from .core import limiter

def create_app(test_config=None) -> Flask:
    
    app = Flask(__name__, instance_relative_config=True)
    limiter.init_app(app)

    CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    register_error_handler(app)
    
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