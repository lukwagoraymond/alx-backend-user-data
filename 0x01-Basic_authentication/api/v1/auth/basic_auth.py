#!/usr/bin/env python3
""" Module of Basic authentication class
"""
import re
import base64
import binascii
from .auth import Auth
from typing import Tuple, TypeVar
from models.user import User


class BasicAuth(Auth):
    """A class that inherits from Auth and implements the
    Basic Authentication methods"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Method that returns the Base64 encoding of the Authorization part
        in Request Header"""
        if type(authorization_header) is str:
            pattern = '^Basic\\s.*$'
            auth_match = re.fullmatch(pattern, authorization_header.strip())
            if auth_match is not None:
                str_list = authorization_header.split()
                return str_list[-1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str)\
            -> str:
        """Method that returns the decoded value of a Base64 string"""
        if type(base64_authorization_header) is str:
            try:
                decoded_bytes = base64.b64decode(base64_authorization_header,
                                                 validate=True)
                return decoded_bytes.decode('utf-8')
            except(binascii.Error, UnicodeDecodeError):
                return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str)\
            -> Tuple[str, str]:
        """Methods returns user email and password
        from the Base64 decoded value"""
        if type(decoded_base64_authorization_header) is str:
            pattern = r'^([^:]+):(.+)$'
            credential_match = re.fullmatch(
                pattern, decoded_base64_authorization_header.strip())
            if credential_match is not None:
                user_email = credential_match.group(1)
                password = credential_match.group(2)
                return user_email, password
        return None, None

    def user_object_from_credentials(self,
                                     user_email: str, user_pwd: str)\
            -> TypeVar('User'):
        """Method returns the user based on email and password"""
        if type(user_email) is str and type(user_pwd) is str:
            try:
                users = User.search({'email': user_email})
            except Exception:
                return None
            if len(users) <= 0:
                return None
            if users[0].is_valid_password(user_pwd):
                return users[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Method that retrieves a User instance of a request"""
        auth_header = self.authorization_header(request)
        base64_auth_token = self.extract_base64_authorization_header(
            auth_header)
        auth_token = self.decode_base64_authorization_header(base64_auth_token)
        user_email, password = self.extract_user_credentials(auth_token)
        return self.user_object_from_credentials(user_email, password)
