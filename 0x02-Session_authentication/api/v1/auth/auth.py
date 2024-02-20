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
        if not path or not excluded_paths or excluded_paths == []:
            return True
        if path[-1] != '/':
            path += '/'
        if path not in excluded_paths:
            return True
        return False

    def authorization_header(
        self,
        request=None
    ) -> str:
        """Return Auth Header if available"""
        if request is not None:
            return request.headers.get('Authorization')
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Fetch the current user
        """
        return None

    def session_cookie(self, request=None) -> str:
        """
        Get value of cookie SESSION_NAME.
        """
        if request is None:
            return None
        cookie_name = os.getenv('SESSION_NAME')
        return request.cookies.get(cookie_name)
