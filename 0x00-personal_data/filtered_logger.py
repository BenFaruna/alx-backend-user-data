#!/usr/bin/env python3
"""module for logging"""
import logging
import re

from typing import List


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str):
    """function returns the log message obfuscated"""
    pattern = f"(?<={separator})(" + "|".join(fields) + f")=(.+?);"
    message = re.sub(pattern, f"{separator}\\1={redaction};", message)
    return re.sub(f"{separator}{{2,}}", f"{separator}", message)
