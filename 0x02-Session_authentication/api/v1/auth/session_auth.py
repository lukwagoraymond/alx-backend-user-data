#!/usr/bin/env python3
""" Module of Session authentication class
"""

from .auth import Auth
from models.user import User
from uuid import uuid4
from flask import request


class SessionAuth(Auth):
    """A class that inherits from Auth and implements the
        Session Authentication methods"""
    user_id_by_session_id = dict()

    def create_session(self, user_id: str = None) -> str:
        """Public Method creates a SessionID for user_id"""
        if isinstance(user_id, str):
            session_id = str(uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Method returns the user_id based on the session_id"""
        if isinstance(session_id, str):
            return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Methods that returns a User instance based on a
        cookie value"""
        user_id = self.user_id_for_session_id(self.session_cookie(request))
        return User.get(user_id)

    def destroy_session(self, request=None):
        """Method that deletes the user session / logout"""
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if (request is None or session_id is None) or user_id is None:
            return False
        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
        return True
