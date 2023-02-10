#!/usr/bin/env python3
"""module containig session authentication logic"""
import os
import uuid

from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """Session authentication class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a Session ID for a user_id"""
        if user_id is None or type(user_id) != str:
            return None

        session_id = str(uuid.uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a User ID based on a Session ID"""
        if session_id is None or type(session_id) != str:
            return None

        return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """returns a User instance based on a cookie value"""
        cookie_key = self.session_cookie(request)
        user_id = self.user_id_by_session_id.get(cookie_key)
        if type(user_id) == dict:
            return User.get(user_id.get('user_id'))
        return User.get(user_id)

    def destroy_session(self, request=None):
        """deletes the user session/logout"""
        if request is None:
            return False
        else:
            session_id = self.session_cookie(request)
            if session_id is None:
                return False
            elif self.user_id_by_session_id.get(session_id) is None:
                return False
            else:
                self.user_id_by_session_id.pop(session_id)
                return True
