#!/usr/bin/env python3
"""module handles all routes for the Session authentication"""
import os

from flask import abort, jsonify, request

from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_auth_login():
    """function handles user login and starting new user session"""
    email = request.form.get('email')
    password = request.form.get('password')

    if email is None:
        return jsonify({"error": "email missing"}), 400
    elif password is None:
        return jsonify({"error": "password missing"}), 400

    user = User.search({'email': email})
    if len(user) > 0:
        user = user[0]

    if type(user) == list and len(user) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    elif not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    else:
        from api.v1.app import auth
        output = jsonify(user.to_json())
        session_id = auth.create_session(user.id)
        output.set_cookie(os.getenv('SESSION_NAME'), session_id)
        return output

@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def session_auth_logout():
    """function handles user logout"""
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    else:
        abort(404)
