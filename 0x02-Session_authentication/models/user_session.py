#!/usr/bin/env python3
""" File based DB Module
"""
from models.base import Base


class UserSession(Base):
    """Class Model that contains methods to store Session_IDs
    in a file based system on local environment"""
    def __init__(self, *args: list, **kwargs: dict):
        """Constructor to initialise User session object
        attributes"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
