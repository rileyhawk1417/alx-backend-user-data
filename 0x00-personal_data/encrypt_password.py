#!/usr/bin/env python3

"""
Module to encrypt password
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hash password using random salt.
    Args:
        str: password
    Returns:
        bytes: password hash
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Check if password is hashed
    Args:
        bytes: hashed_password
        str: password
    Returns:
        bool: If hashed True else False
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
