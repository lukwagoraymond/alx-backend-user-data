#!/usr/bin/env python3
""" Module of Session Expiration class
"""

from .session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """A class that inherits from SessionAuth and implements the
        Session Expiration methods"""

    def __init__(self):
        """Constructor for SessionExpiration"""
        try:
            self.session_duration = int(getenv('SESSION_DURATION', '0'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Method inherits create_session from sessionAuth class"""
        session_id = super().create_session(user_id)
        if session_id:
            session_dictionary = dict()
            session_dictionary.update({'user_id': user_id,
                                       'created_at': datetime.now()})
            self.user_id_by_session_id.update({session_id: session_dictionary})
            return session_id
        return None

    def user_id_for_session_id(self, session_id=None):
        """Generates user_id based on a particular session_id"""
        if session_id in self.user_id_by_session_id:
            session_dictionary = self.user_id_by_session_id.get(session_id)
            if self.session_duration <= 0:
                return session_dictionary.get('user_id')
            if 'created_at' not in session_dictionary:
                return None
            ini_time_for_now = datetime.now()
            time_duration = timedelta(seconds=self.session_duration)
            expiration_time = session_dictionary['created_at'] + time_duration
            if expiration_time < ini_time_for_now:
                return None
            return session_dictionary.get('user_id')
