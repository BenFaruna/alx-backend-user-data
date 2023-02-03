#!/usr/bin/env python3
"""module for logging"""
import logging
import re
import os

import mysql.connector as mysql

from typing import List

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
        ) -> str:
    """function returns the log message obfuscated"""
    pattern = f"(?<={separator})(" + "|".join(fields) + f")=(.+?);"
    message = re.sub(pattern, f"{separator}\\1={redaction};", message)
    return re.sub(f"{separator}{{2,}}", f"{separator}", message)


def get_logger() -> logging.Logger:
    """function creates a Logger with a StreamHandler
    using RedactingFormatter as formatter
    """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)

    formatter = RedactingFormatter(PII_FIELDS)

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def get_db() -> mysql.connection.MySQLConnection:
    """function uses runtime variables to access database and
    return a connector"""
    connection = mysql.connect(
        host=os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        user=os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        database=os.getenv('PERSONAL_DATA_DB_NAME'),
    )
    return connection


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """function for initializing the class"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """formats log and redacts some fields"""
        message = filter_datum(
            self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR
            )
        record.msg = message
        return super().format(record)


def main() -> None:
    """function will obtain a database connection using get_db and retrieve
    all rows in the users table and display each row under a filtered"""
    logger = get_logger()
    db_connect = get_db()
    cur = db_connect.cursor()
    cur.execute('SHOW COLUMNS FROM users;')
    columns = []
    for column in cur.fetchall():
        columns.append(column[0])

    cur.execute('SELECT * FROM users;')
    for row in cur.fetchall():
        data = []
        message = ''
        row = list(row)
        row[6] = row[6].strftime('%Y-%m-%d %H:%M:%S')
        for i in range(len(row)):
            data.append(f'{columns[i]}={row[i]}')
        message = ';'.join(data)
        message += ';'

        logger.info(message)


if __name__ == '__main__':
    main()
