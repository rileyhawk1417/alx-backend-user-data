#!/usr/bin/env python3

"""Module to showcase basic auth"""

import base64
from typing import Tuple, TypeVar

from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """
    Class inherits from Auth
    & handles everything auth related
    """

    def extract_base64_authorization_header(
        self,
        authorization_header: str
    ) -> str:
        """
        Return Base64 encoded part of Auth header
        Args:
             str: authorization_header
        Returns:
            str: base64 of auth header
        """
        if not (authorization_header and
                isinstance(authorization_header, str)
                and authorization_header.startswith('Basic ')):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
        self,
        base64_authorization_header: str
    ) -> str:
        """
        Return Base64 decoded part of Auth header
        Args:
             str: base64_authorization_header
        Returns:
            str: decoded base64 of auth header
        """
        if not (base64_authorization_header and
                isinstance(base64_authorization_header, str)):
            return None
        try:
            decoded_data = base64.b64decode(base64_authorization_header)
            return decoded_data.decode('utf-8')
        except BaseException:
            return None

    def extract_user_credentials(
        self,
        decoded_base64_authorization_header: str
    ) -> str:
        """
        Return user email & password
        Args:
             str: decoded_base64_authorization_header
        Returns:
            tuple: tuple (str, str)
        """
        if not (decoded_base64_authorization_header and
                isinstance(decoded_base64_authorization_header, str)
                and ':' in decoded_base64_authorization_header):
            return None, None
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(
        self,
        user_email: str,
        user_pwd: str
    ) -> TypeVar('User'):
        """
        Return specified user email & password
        Args:
             str: user_email
             str: user_pwd
        Returns:
            User: return User obj if found else None
        """
        if not (user_email and
                isinstance(user_email, str)
                and user_pwd and isinstance(user_pwd, str)):
            return None

        try:
            users_list = User.search({'email': user_email})
        except Exception:
            return None

        for user in users_list:
            if user.is_valid_password(user_pwd):
                return user

        return None
    # Sure it overrides the other class though not correctly

    def current_user(
        self,
        request: None
    ) -> TypeVar('User'):
        """
        Return specified user email & password
        Args:
             None: request
        Returns:
            User: return User obj if found else None
        """
        try:
            auth_header = self.authorization_header(request)
            encoded = self.extract_base64_authorization_header(auth_header)
            decoded = self.decode_base64_authorization_header(encoded)
            email, password = self.extract_user_credentials(decoded)
            return self.user_object_from_credentials(email, password)
        except Exception:
            return None
