#!/usr/bin/env python3

"""
Session Authentication Module
That manages time based sessions.
"""

from os import getenv
from datetime import datetime, timedelta
from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """
    SessionAuth class to manage a session
    With expiry time
    """

    def __init__(self) -> None:
        super().__init__()
        try:
            self.session_duration = int(getenv('SESSION_DURATION', '0'))
        except Exception:
            self.session_duration = 0
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Create a session for the user
        Args:
            user_id: str
        Returns:
            user_id: str
        """
        session_id = super().create_session(user_id)
        if session_id and isinstance(session_id, str):
            self.user_id_by_session_id[session_id] = {
                'user_id': user_id,
                'created_at': datetime.now()
            }
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
        sess_id = self.user_id_by_session_id
        if session_id in sess_id:
            session = sess_id[session_id]
            if self.session_duration <= 0:
                return session['user_id']
            if 'created_at' not in session:
                return None
            now_time = datetime.now()
            time_diff = timedelta(seconds=self.session_duration)
            exp_time = session['created_at'] + time_diff
            if exp_time < now_time:
                return None
            return session['user_id']
        return None
