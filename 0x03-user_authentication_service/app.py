#!/usr/bin/env python3
"""Module contains Flask App"""

from flask import Flask, jsonify, \
    request, make_response, abort, \
    redirect
from auth import Auth

AUTH = Auth()

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home_page() -> str:
    """_summary_ index page"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """_summary_ creation of users"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user_obj = AUTH.register_user(email, password)
        return jsonify({"email": user_obj.email,
                        "message": "user created"}), 200
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """logins in user and creates a session_id"""
    email = request.form.get('email')
    password = request.form.get('password')

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        resp = make_response({"email": email, "message": "logged in"})
        resp.set_cookie('session_id', session_id)
        return resp, 200
    return abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """logouts a user out of a session & redirects to home-page"""
    session_id = request.cookies.get('session_id')
    user_obj = AUTH.get_user_from_session_id(session_id)
    if user_obj is not None:
        AUTH.destroy_session(user_obj.id)
        return redirect('/')
    else:
        abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """based on the session_id returns user obj email"""
    session_id = request.cookies.get('session_id')
    user_obj = AUTH.get_user_from_session_id(session_id)
    if user_obj is not None:
        return jsonify({"email": user_obj.email}), 200
    else:
        return abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """checks for email & generates token"""
    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token}), 200
    except Exception:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """for a corresponding user to an email, reset_token
    update the password"""
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
