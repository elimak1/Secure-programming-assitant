import functools
import logging

from flask import (
    Blueprint, g,  request, session, Response, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

from api.db.db_utils import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=("POST", "GET"))
def register():
    if request.method == 'POST':
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        confirm_password = request.json.get('confirmPassword', None)
        email = request.json.get('email', None)

        db = get_db()
        error = None

        # TODO: USERNAME AND PASSWORD VALIDATION 
        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif not email:
            error = "Email is required."
        elif password != confirm_password:
            error = "Passwords do not match."

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password, email) VALUES (?, ?, ?)",
                    (username, generate_password_hash(password), email),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                user = db.execute(
                    'SELECT * FROM user WHERE username = ?', (username,)
                    ).fetchone()
                if user is None:
                    error = 'Server error.'
                else:
                    session.clear()
                    session['user_id'] = user['id']
                    return jsonify({'username': username})
        return Response(error, status=400)

    logging.error(error)

    return Response(status=400)

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return jsonify({'username': username})
        return Response(error, status=400)
    
    return Response(status=400)

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
def user():
    if g.user is None:
        return Response(status=401)
    return jsonify({'username': g.user['username']})

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return Response(status=401)

        return view(**kwargs)

    return wrapped_view
