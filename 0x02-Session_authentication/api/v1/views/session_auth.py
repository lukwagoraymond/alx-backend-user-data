#!/usr/bin/env python3
""" Module for session_auth views
"""
from typing import Tuple
from os import getenv
from models.user import User
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> Tuple[str, int]:
    """ POST /api/v1/auth_session/login
        Return:
          - User object JSON represented
        """
    email = request.form.get("email")
    password = request.form.get("password")
    if email is None or email == '':
        return jsonify({"error": "email missing"}), 400
    if password == '' or password is None:
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if len(users) <= 0 or not users:
        return jsonify({"error": "no user found for this email"}), 404
    if users[0].is_valid_password(password):
        from api.v1.app import auth
        user_id = getattr(users[0], 'id')
        sess_id = auth.create_session(user_id)
        res_obj = jsonify(users[0].to_json())
        res_obj.set_cookie(getenv("SESSION_NAME"), sess_id)
        return res_obj
    return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def session_logout() -> Tuple[str, int]:
    """
    DELETE /api/v1/auth_session/logout
    Returns:
        - An empty JSON object
    """
    from api.v1.app import auth
    logd_out_session = auth.destroy_session(request)
    if not logd_out_session:
        abort(404)
    return jsonify({}), 200
