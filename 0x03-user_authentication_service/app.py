#!/usr/bin/env python3
"""Module contains Flask App"""

from flask import Flask, jsonify, request

from auth import Auth

AUTH = Auth()

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home_page() -> str:
    """_summary_ index page"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def create_users() -> str:
    """_summary_ creation of users"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user_obj = AUTH.register_user(email, password)
        return jsonify({"email": user_obj.email, "message": "user created"}), 200
    except Exception:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
