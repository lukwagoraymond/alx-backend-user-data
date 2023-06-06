#!/usr/bin/env python3
"""Module contains Auth middleware"""

import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """generates a hashed password"""
    string = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(string, salt)
    return hashed_pwd


def _generate_uuid():
    """Generates a random string representation"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """saves a user instance into the DB with hashed password"""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_passwrd = _hash_password(password)
            user_obj = self._db.add_user(email=email, hashed_password=hashed_passwrd)
            return user_obj
        else:
            raise ValueError(f'User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        """validates login credentials and returns boolean"""

        password = password.encode('utf-8')
        try:
            user_obj = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        if bcrypt.checkpw(password, user_obj.hashed_password):
            return True
        return False

    def create_session(self, email: str) -> str:
        """Finds a user object corresponding to an
        email and then returns a session id"""
        try:
            user_obj = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        else:
            user_obj.session_id = _generate_uuid()
            return user_obj.session_id
