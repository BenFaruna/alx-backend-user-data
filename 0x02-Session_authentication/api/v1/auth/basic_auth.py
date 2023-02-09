#!/usr/bin/env python3
"""module implementing Basic Authentication"""
import base64

from typing import Tuple, TypeVar

from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """class implementing basic authentication"""
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """extract the base64 part of the authorization header"""
        if authorization_header is None or type(authorization_header) != str:
            return None

        header_list = authorization_header.split()
        if header_list[0] == 'Basic' and len(header_list) > 1:
            return header_list[1]

        return None

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """decode a base64 string to utf8"""
        if (base64_authorization_header is None) or (
                type(base64_authorization_header) != str):
            return None

        try:
            return base64.b64decode(
                base64_authorization_header).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """returns the user email and password from the Base64 decoded value"""
        if decoded_base64_authorization_header is None:
            return None, None
        elif type(decoded_base64_authorization_header) != str:
            return None, None

        email_pass = decoded_base64_authorization_header.split(':', 1)
        if len(email_pass) != 2:
            return None, None

        return tuple(email_pass)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """returns the User instance based on his email and password"""
        if user_email is None or type(user_email) != str:
            return None
        elif user_pwd is None or type(user_email) != str:
            return None

        if User.count() == 0:
            return None
        else:
            user = User.search({'email': user_email})
            if len(user) == 0:
                return None

            user = user[0]
            if user.is_valid_password(user_pwd):
                return user

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """overloads Auth and retrieves the User instance for a request"""
        auth_header = self.authorization_header(request)
        auth_header = self.extract_base64_authorization_header(auth_header)
        auth_header = self.decode_base64_authorization_header(auth_header)

        user_credentials = self.extract_user_credentials(auth_header)
        user = self.user_object_from_credentials(*user_credentials)
        return user
