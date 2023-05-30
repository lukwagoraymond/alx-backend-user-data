#!/usr/bin/env python3
""" Module of authentication class
"""

import re
from flask import request
from typing import List, TypeVar


class Auth:
    """Class to manage the API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Public Method that checks if
        the path requires authentication
        Returns:
            False if path is in List"""
        if path is not None and excluded_paths is not None:
            new_path = f'{path}/' if not path.endswith('/') else path
            pattern = f'^{new_path}$'
            if len(excluded_paths) > 0:
                for route in excluded_paths:
                    if bool(re.search(pattern, route)) is True:
                        return False
        return True

    def authorization_header(self, request=None) -> str:
        """Method gets the authorisation header from
        the request; request is Flask request Object"""
        if request is not None:
            return request.headers.get('Authorization', None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Method gets current user from the request"""
        return None
