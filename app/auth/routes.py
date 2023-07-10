from flask import json, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from sqlalchemy.exc import IntegrityError

from app.models.blacklist_token import BlacklistToken
from app.models.user import Users
from app.extensions import db, jwt
from app.auth import authBp


# Register
@authBp.route('/register', methods=['POST'], strict_slashes=False)
def register():
    data = request.get_json()

    username = data.get('username', None)
    email = data.get('email', None)
    password = generate_password_hash(data.get('password', None))

    # Required
    if not username or not email or not password:
        return jsonify({
            "message": "Username, email and password are required!"
        }), 400

    # Username or email cant same
    try:
        db.session.add(Users(username=username, email=email, password=password))
        db.session.commit()
    except IntegrityError:
        return jsonify({
            "message": "User already exist, try other username/email"
        }), 422

    return jsonify({
        "message": "User has been registered sucessfully"
    }), 200


# Login
@authBp.route('/login', methods=['POST'], strict_slashes=False)
def login():
    data = request.get_json()

    email = data.get('email', None)
    password = data.get('password', None)


    if not email or not password:
        return jsonify({
            "message": "Email or password are required!"
        }), 422

    user = Users.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({
            "message": "Username or password is invalid!",
        }), 422

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    return jsonify({
        "message": "Login success",
        "access_token": access_token,
        "refresh_token": refresh_token
    }), 200


# Refresh Token
@authBp.route('/refresh', methods=['POST'], strict_slashes=False)
@jwt_required(refresh=True)
def refresh_token():
    user = get_jwt_identity()
    access_token = {
        "access_token": create_access_token(identity=user)
    }

    return jsonify(access_token), 200


# Logout
@authBp.route('/logout', methods=['POST'], strict_slashes=False)
@jwt_required(locations=['headers'])
def logout():
    raw_jwt = get_jwt()
    jti = raw_jwt.get('jti')
    token = BlacklistToken(jti=jti)

    db.session.add(token)
    db.session.commit()

    return jsonify({
        "message": "User have been logged out!"
    }), 200


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token = BlacklistToken.query.filter_by(jti=jti).first()

    return token is not None