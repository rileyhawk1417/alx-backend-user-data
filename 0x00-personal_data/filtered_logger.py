#!/usr/bin/env python3

"""
Module to filter logs
"""

import os
import re
import logging
import mysql.connector
from typing import List

patterns = {
    'extract': lambda x, y: r'(?P<field>{})=[^{}]*'.format('|'.join(x), y),
    'replace': lambda x: r'\g<field>={}'.format(x)
}
PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """
    Filter fields & add separators
    Args:
        List[str]: fields
        str: redaction
        str: message
        str: separator
    Returns:
        str: formatted data
    """
    extract, replace = (patterns['extract'], patterns['replace'])
    return re.sub(extract(fields, separator), replace(redaction), message)


def get_logger() -> logging.Logger:
    """
    Create new logger for user data
    Returns:
        logging.Logger: Log record
    """
    logger = logging.getLogger('user_data')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Create a mysql connection to database
    """
    db_host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME', '')
    db_user = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    db_pass = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    connection = mysql.connector.connect(
        host=db_host,
        port=3306,
        user=db_user,
        password=db_pass,
        database=db_name
    )
    return connection


def entryPoint():
    """
    Log information about user
    """
    fields = 'name,email,phone,ssn,password,ip,last_login,user_agent'
    columns = fields.split(',')
    query = 'SELECT {} FROM users'.format(fields)
    logger = get_logger()
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            record = map(
                lambda x: '{}={}'.format(x[0], x[1]),
                zip(columns, row)
            )
            msg = '{};'.format('; '.join(list(record)))
            args = ('user_data', logging.INFO, None, None, msg, None, None)
            log_entry = logging.LogRecord(*args)
            logger.handle(log_entry)


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter
    """
    REDACTION = '***'
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    FORMAT_FIELDS = ('name', 'levelname', 'asctime', 'message')
    SEPARATOR = ';'

    def __init__(self, fields: List[str]) -> None:
        """
        Init method for class
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format a log Record"""
        msg = super(RedactingFormatter, self).format(record)
        output = filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
        return output


if __name__ == '__main__':
    entryPoint()
