#!/usr/bin/env python3
""" Module of Session DB Storage class
"""
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """A class that inherits from Session Expiration
    and contains DB Storage Authentication Methods"""

    def create_session(self, user_id=None):
        """Creates and Stores a new object of UserSession
        then returns a session ID"""
        session_id = super().create_session(user_id)
        if isinstance(session_id, str):
            kwargs = {'user_id': user_id, 'session_id': session_id}
            user_session = UserSession(**kwargs)
            user_session.save()
            return session_id

    def user_id_for_session_id(self, session_id=None):
        """Returns user_id when user session id is used"""
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(sessions) <= 0:
            return None
        return sessions[0].user_id

    def destroy_session(self, request=None):
        """Method Destroys a user session based on a session ID
        from a request cookie"""
        session_id = self.session_cookie(request)
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return False
        if len(sessions) <= 0:
            return False
        sessions.clear()
        return True
