from flask import (
    Blueprint, g,  request, session, Response, jsonify
)
from api.authenticate import getResourceProtector

bp = Blueprint('auth', __name__, url_prefix='/auth')

require_auth = getResourceProtector()

@bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return Response(status=200)

@bp.route('/user', methods=['GET'])
@require_auth(None)
def user():
    token = require_auth.acquire_token()
    print(token)
    return jsonify({'userId': token.get('sub')})
