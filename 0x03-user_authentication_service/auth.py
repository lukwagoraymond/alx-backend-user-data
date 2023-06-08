#!/usr/bin/env python3
"""Module contains Auth middleware"""

import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from typing import Union


def _hash_password(password: str) -> bytes:
    """generates a hashed password"""
    string = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(string, salt)
    return hashed_pwd


def _generate_uuid() -> str:
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
            user_obj = self._db.add_user(email=email,
                                         hashed_password=hashed_passwrd)
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

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Searches for user object present based on session_id"""
        if session_id is not None:
            try:
                user_obj = self._db.find_user_by(session_id=session_id)
                return user_obj
            except NoResultFound:
                return None
        return None

    def destroy_session(self, user_id: str) -> None:
        """Updates the corresponding session_id of
        that user object to None"""
        if user_id is not None:
            self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """Finds user corresponding to the email & generates
        a UUID for the reset token"""
        try:
            user_obj = self._db.find_user_by(email=email)
            token = _generate_uuid()
            self._db.update_user(user_obj.id, reset_token=token)
            return token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """Find user corresponding to the reset_token
        & updates the password with new hashed
        password"""
        try:
            user_obj = self._db.find_user_by(reset_token=reset_token)
            hashed_passwrd = _hash_password(password)
            self._db.update_user(user_obj.id,
                                 hashed_password=hashed_passwrd,
                                 reset_token=None)
            return None
        except NoResultFound:
            raise ValueError
