#!/usr/bin/env python3
"""module implementing session expiring autentication"""
import os

from datetime import datetime, timedelta

from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """class adds expiration date to a Session ID"""
    def __init__(self):
        duration = os.getenv('SESSION_DURATION')
        try:
            self.session_duration = int(duration)
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """creates a Session ID for a user_id"""
        session_id = super().create_session(user_id)

        if not session_id:
            return None
        else:
            session_dictionary = {
                'user_id': user_id,
                'created_at': datetime.now(),
            }
            SessionExpAuth.user_id_by_session_id[
                session_id] = session_dictionary

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """returns a User ID based on a Session ID"""
        if session_id is None:
            return None
        elif session_id not in SessionExpAuth.user_id_by_session_id:
            return None
        else:
            session_dictionary = SessionExpAuth.user_id_by_session_id[
                session_id]
            if self.session_duration <= 0:
                return session_dictionary['user_id']
            elif 'created_at' not in session_dictionary:
                return None
            elif (
                    (session_dictionary['created_at'] +
                     timedelta(seconds=self.session_duration)).timestamp()
                     ) < (datetime.now().timestamp()):
                return None

            return session_dictionary.get('user_id')
