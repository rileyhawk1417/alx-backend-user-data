#!/usr/bin/env python3
"""
Module for authentication
"""
from typing import List, TypeVar
import os

from flask import Flask


class Auth:
    """
    Class to handle everything related to Auth
    """

    def require_auth(
        self,
        path: str,
        excluded_paths: List[str],
    ) -> bool:
        """
        Check if auth path(url) is valid
        """
        if path is None or excluded_paths is None or not excluded_paths:
            return True
        # Handle slash
        if path[-1] == '/':
            path = path[:-1]
        has_slash = False
        for excluded_path in excluded_paths:
            if excluded_path[-1] == '/':
                excluded_path = excluded_path[:-1]
                has_slash = True

            if excluded_path.endswith('*'):
                pos_after_slash = excluded_path.rfind('/') + 1
                excluded = excluded_path[pos_after_slash:-1]

                pos_after_slash = path.rfind('/') + 1
                tmp_path = path[pos_after_slash:]
                if excluded in tmp_path:
                    return False
            if has_slash:
                has_slash = False
        path += '/'

        if path in excluded_paths:
            return False
        return True

    def authorization_header(
        self,
        request=None
    ) -> str:
        """Return Auth Header if available"""
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(
        self,
        request=None
    ) -> TypeVar('User'):
        """
        Fetch the current user
        """
        request = Flask(__name__)
        return None

    def session_cookie(self, request=None) -> str:
        """
        Get value of cookie SESSION_NAME.
        """
        if request is not None:
            cookie_name = os.getenv('SESSION_NAME')
            return request.cookies.get(cookie_name)
