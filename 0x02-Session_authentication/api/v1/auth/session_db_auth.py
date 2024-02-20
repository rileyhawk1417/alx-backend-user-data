
#!/usr/bin/env python3

"""
Session Authentication Module
"""

from flask.app import timedelta

from flask.json import datetime

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionAuth(SessionExpAuth):
    """
    SessionAuth class to manage a session
    """

    def create_session(self, user_id: str = None) -> str:
        """
        Create a session for the user
        Args:
            user_id: str
        Returns:
            user_id: str
        """
        session_id = super().create_session(user_id)
        if user_id and isinstance(user_id, str):
            kwargs = {
                'user_id': user_id,
                'session_id': session_id
            }
            user_sess = UserSession(**kwargs)
            user_sess.save()
            return session_id
        return None

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Fetch user id of specified session
        Args:
            session_id: str
        Returns:
            user_id: str
        """
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if sessions is None or sessions == []:
            return None
        time_now = datetime.now()
        time_diff = timedelta(seconds=self.session_duration)
        exp_time = sessions[0].created_at + time_diff
        if exp_time < time_now:
            return None
        return sessions[0].user_id

    def destroy_session(self, request=None):
        """
        Destroy session related to user
        Args:
            request: (flask) request
        Returns:
            bool: if deleted return true else false
        """
        session_id = self.session_cookie(request)
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return False
        if len(sessions) <= 0:
            return False
        sessions[0].remove()
        return True
