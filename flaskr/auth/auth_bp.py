from flask import Blueprint, request, escape, abort, jsonify
from ..auth.auth import validate_user_data, generate_token
from ..models.user import User
from ..db import db
import bcrypt

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['POST'])
def register():
    user_data = request.get_json()

    user_data['name'] = escape(user_data['name'])
    user_data['email'] = escape(user_data['email'])

    is_current_user = User.query.filter_by(email=user_data['email']).all()
    if is_current_user:
        abort(403)

    if not validate_user_data(user_data):
        abort(400)

    salt = bcrypt.gensalt()
    password = user_data['password'].encode('utf-8')
    hashed_password = bcrypt.hashpw(password, salt)

    new_user = User(
        name=user_data['name'], email=user_data['email'], password=hashed_password.decode())
    db.session.add(new_user)
    db.session.commit()

    payload = {
        "id": new_user.id,
        "email": new_user.email
    }

    token = generate_token(payload)

    return jsonify({"token": token.decode()})


@bp.route('/login', methods=['POST'])
def login():
    user_data = request.get_json()

    email = escape(user_data['email'])
    password = user_data['password'].encode('utf-8')

    result = User.query.filter_by(email=email).all()
    if not result:
        return abort(401)

    user = result[0]

    password_check = bcrypt.checkpw(password, user.password.encode('utf-8'))
    if not password_check:
        return abort(401)

    payload = {
        "id": user.id,
        'email': user.email
    }
    token = generate_token(payload)

    return jsonify({'token': token.decode()})
