#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

auth_t = getenv('AUTH_TYPE', auth)

if auth_t == 'auth':
    auth = Auth()
if auth_t == 'basic_auth':
    auth = BasicAuth()
if auth_t == 'session_auth':
    auth = SessionAuth()


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def req_unauthorised(e) -> str:
    """Unauthorised Client Handler"""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def req_forbidden(e) -> str:
    """forbidden page for authenticated user"""
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def req_filter():
    """Filters requests before processing requests"""
    if auth:
        req_path = request.path
        exclusion_path = ['/api/v1/status/',
                          '/api/v1/unauthorized/',
                          '/api/v1/forbidden/',
                          '/api/v1/auth_session/login/']
        state_path = auth.require_auth(req_path, exclusion_path)
        if state_path:
            user = auth.current_user(request)
            if auth.authorization_header(request) is None \
                    and auth.session_cookie(request) is None:
                abort(401)
            if user is None:
                abort(403)
            request.current_user = user


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
