#!/usr/bin/env python3
"""
Module contains code block to End-to-End Integration Test
"""

import requests


def register_user(email: str, password: str) -> None:
    """Function that signs up a user into the database
    based on their submitted email & password"""
    payload = {'email': email, 'password': password}
    resp = requests.post('http://127.0.0.1:5000/users', data=payload)
    r_status = resp.status_code
    assert r_status == 200
    assert resp.json() == {"email": email, "message": "user created"}
    resp = requests.post('http://127.0.0.1:5000/users', data=payload)
    assert resp.status_code == 400
    assert resp.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Logins in a user with a wrong password"""
    payload = {'email': email, 'password': password}
    resp = requests.post('http://127.0.0.1:5000/sessions', data=payload)
    r_status = resp.status_code
    assert r_status == 401


def log_in(email: str, password: str) -> str:
    """Logs in a user into the system"""
    payload = {'email': email, 'password': password}
    resp = requests.post('http://127.0.0.1:5000/sessions', data=payload)
    r_status = resp.status_code
    assert r_status == 200
    assert resp.json() == {"email": email, "message": "logged in"}
    return resp.cookies['session_id']


def profile_unlogged() -> None:
    """Test when no session_id is supplied when checking for
    profile of logged-in user"""
    resp = requests.get('http://127.0.0.1:5000/profile')
    assert resp.status_code == 403


def profile_logged(session_id: str) -> None:
    """Display back the profile of the logged-in user"""
    resp = requests.get('http://127.0.0.1:5000/profile',
                        cookies={'session_id': session_id})
    assert resp.status_code == 200
    assert 'email' in resp.json()


def log_out(session_id: str) -> None:
    """Logs a user out of the system if they are
    signed in"""
    resp = requests.delete('http://127.0.0.1:5000/sessions',
                           cookies={'session_id': session_id})
    r_status = resp.status_code
    assert r_status == 200
    assert resp.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """This function generates a token when one needs
    to update their password to a new one"""
    payload = {'email': email}
    resp = requests.post('http://127.0.0.1:5000/reset_password', data=payload)
    r_status = resp.status_code
    assert r_status == 200
    assert 'email' in resp.json()
    assert 'reset_token' in resp.json()
    assert resp.json().get('email') == email
    return resp.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Updates an old password to a new password if the
    user has a generated reset token included on him"""
    payload = {'email': email,
               'reset_token': reset_token,
               'new_password': new_password,
               }
    resp = requests.put('http://127.0.0.1:5000/reset_password', data=payload)
    assert resp.status_code == 201
    assert resp.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
