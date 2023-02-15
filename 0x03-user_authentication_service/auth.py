#!/usr/bin/env python3
"""module containing authentication functions and class"""
import bcrypt
import uuid

from typing import Union

from sqlalchemy.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """hash password and returns bytes"""
    salt = bcrypt.gensalt()
    hash_pw = bcrypt.hashpw(password.encode(), salt)
    return hash_pw


def _generate_uuid() -> str:
    """return a string representation of a new UUID"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str = None, password: str = None) -> User:
        """method saves the user to the database and return the User object"""
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')
        except NoResultFound:
            password = _hash_password(password)
            user = self._db.add_user(email, password)
        return user

    def valid_login(self, email: str = None, password: str = None) -> bool:
        """check email if it matches an entry in the db and returns boolean"""
        try:
            user = self._db.find_user_by(email=email)
            match = bcrypt.checkpw(password.encode(), user.hashed_password)
            return match
        except NoResultFound:
            return False

    def create_session(self, email) -> Union[str, None]:
        """returns the session ID as a string"""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(
            self, session_id: str = None) -> Union[User, None]:
        """takes session_id and returns the corresponding User or None"""
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """method updates the corresponding user’s session ID to None"""
        self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """take an email string argument and returns a UUID string"""
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token, password) -> None:
        """hash the password and update the user’s hashed_password field
        with the new hashed password and the reset_token field to None"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            password = _hash_password(password)
            self._db.update_user(
                user.id, hashed_password=password, reset_token=None)
        except NoResultFound:
            raise ValueError
