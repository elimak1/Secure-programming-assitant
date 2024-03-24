from flask import (
    Blueprint, g,  request, session, Response, jsonify
)
from api.db.db_utils import get_db
from api.authenticate import getResourceProtector

bp = Blueprint('auth', __name__, url_prefix='/auth')

require_auth = getResourceProtector()

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

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
