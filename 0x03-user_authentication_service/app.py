#!/usr/bin/env python3
"""module for flask app and routing"""
from flask import Flask, abort, redirect, request, jsonify

from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route('/')
def home():
    """route to home page"""
    return jsonify({'message': 'Bienvenue'})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """endpoint registers user and save details in database"""
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        AUTH.register_user(email, password)
        return jsonify({'email': email, 'message': 'user created'})
    except ValueError:
        return jsonify({'message': 'email already registered'}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """endpoint for user login"""
    email = request.form.get('email')
    password = request.form.get('password')

    correct_details = AUTH.valid_login(email, password)

    if correct_details:
        session_id = AUTH.create_session(email)
        output = jsonify({'email': email, 'message': 'logged in'})
        output.set_cookie('session_id', session_id)
        return output

    return abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """endpoint for user logout"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    abort(403)


@app.route('/profile', strict_slashes=False)
def profile():
    """endpoint for viewing user profile"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    return jsonify({'email': user.email})


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """endpoint for getting token for password reset"""
    email = request.form.get('email')

    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({'email': email, 'reset_token': reset_token})
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """endpoint for updating user password"""
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({'email': email, 'message': 'Password updated'})
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
