#!/usr/bin/env python3

"""
Session Authentication Module
"""

from uuid import uuid4
from .auth import Auth
from models.user import User


class SessionAuth(Auth):
    """
    SessionAuth class to manage a session
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Create a session for the user
        Args:
            user_id: str
        Returns:
            user_id: str
        """
        if isinstance(user_id, str):
            session_id = str(uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Fetch user id of specified session
        Args:
            session_id: str
        Returns:
            user_id: str
        """
        if isinstance(session_id, str):
            return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> User:
        """
        Fetch user related to request
        Args:
            request: (flask) request
        Returns:
            user: User
        """
        user_id = self.user_id_for_session_id(self.session_cookie(request))
        return User.get(user_id)

    def destroy_session(self, request=None):
        """
        Destroy session related to user
        Args:
            request: (flask) request
        Returns:
            bool: if deleted return true else false
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if (request is None or session_id is None) or user_id is None:
            return False
        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
        return True
