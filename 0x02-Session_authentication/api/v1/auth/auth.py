#!/usr/bin/env python3
"""module for authentication"""
import os

from flask import request

from typing import List, TypeVar


class Auth:
    """template for all authentication systems"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns a boolean for routes that require authentication"""
        for ex_paths in excluded_paths:
            if ex_paths.endswith('*'):
                if path.startswith(ex_paths[:-1]):
                    return False

        if (path is not None) and (not path.endswith('/')):
            path = path + '/'

        if path is None or excluded_paths is None:
            return True
        elif path not in excluded_paths:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """returns str to be added to authorization header"""
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """returns the current user"""
        return None

    def session_cookie(self, request=None):
        """returns a cookie value from a request"""
        if request is None:
            return None

        cookie_name = os.getenv('SESSION_NAME', '_my_session_id')

        return request.cookies.get(cookie_name)
