#!/usr/bin/env python3
"""Module containing function methods for logging and
password security encryption"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Implements a bcrypt salted hashed password encryption
    Args:
        password: Byte String containing password
    Returns:
        A hashed byte password"""
    byte_string = password.encode('utf-8')
    return bcrypt.hashpw(byte_string, bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """function validates that the provided password matches the
    hashed password
    Args:
        hashed_password: the hashed produced password
        password: the original password
    Return:
        True or False
        """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
