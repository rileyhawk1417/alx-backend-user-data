#!/usr/bin/env python3

"""
Module to filter logs
"""

import re
import logging
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


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter
    """
    REDACTION = '***'
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    FORMAT_FIELDS = ('name', 'levelname', 'asctime', 'message')
    SEPARATOR = ';'

    def __init__(self, fields) -> None:
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
