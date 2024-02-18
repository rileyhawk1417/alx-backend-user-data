#!/usr/bin/env python3
"""
Module for authentication
"""
from typing import List, TypeVar
import os

from flask import Flask
import re


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
        if path is not None and excluded_paths is not None:
            for excluded in map(lambda v: v.strip(), excluded_paths):
                pattern = ''
                if excluded[-1] == '*':
                    pattern = f'{excluded[0:-1]}.*'
                elif excluded[-1] == '/':
                    pattern = f'{excluded[0:-1]}/*'
                else:
                    pattern = f'{excluded}/*'
                if re.match(pattern, path):
                    return False
        return False

    def authorization_header(
        self,
        request=None
    ) -> str:
        """Return Auth Header if available"""
        if request is not None:
            return request.headers.get('Authorization')
        return None

    def current_user(
        self,
        request=None
    ) -> TypeVar('User'):
        """
        Fetch the current user
        """
        return None

    def session_cookie(self, request=None) -> str:
        """
        Get value of cookie SESSION_NAME.
        """
        if request is not None:
            cookie_name = os.getenv('SESSION_NAME')
            return request.cookies.get(cookie_name)
