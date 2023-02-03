#!/usr/bin/env python3
"""module for encrypting password"""
import bcrypt


def hash_password(password: str) -> bytes:
    """creates a password hash from the password argument"""
    salt = bcrypt.gensalt()
    hashpw = bcrypt.hashpw(password.encode(), salt)
    return hashpw


def is_valid(hashed_password: bytes, password: str) -> bool:
    """checks password if it matches the hashed password"""
    validity = bcrypt.checkpw(password.encode(), hashed_password)
    return validity
