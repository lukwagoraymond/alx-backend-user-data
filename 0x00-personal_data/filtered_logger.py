#!/usr/bin/env python3
"""Module containing function methods for logging and
password security encryption"""
from typing import List, Tuple
import os
import re
import logging
import mysql.connector

PII_FIELDS = ('name', 'email', 'phone', 'password', 'ssn')


def filter_datum(fields: List[str],
                 redaction: str, message: str,
                 separator: str) -> str:
    """Replaces sensitive information in a message log
    with a redacted value based on the list of fields to
    redact
    Args:
        fields: list of fields to redact
        redaction: the value to use for redaction
        message: the string message to filter
        separator: the separator to use between fields
    Returns:
        The filtered string message with redacted values"""
    """x = message.rsplit(separator)
        x_len = len(x)

        for k_val in range(x_len - 1):
            for checks in fields:
                if x[k_val].startswith(checks):
                    y_list = x[k_val].rsplit('=')
                    x[k_val] = x[k_val].replace(y_list[1], redaction)
                else:
                    continue
        x = separator.join(x)
        return x"""
    for field in fields:
        message = re.sub(f'{field}=(?<==)[^;]+{separator}',
                         f'{field}={redaction}{separator}', message)
    return message


def get_logger() -> logging.Logger:
    """Function that creates a logger object named
    user_data, logs upto INFO, contains a streamhandler
    that includes same RedactingFormatter"""
    # Create our demo logger
    logger = logging.getLogger('user_data')
    # Set a log level for the logger
    logger.setLevel(logging.INFO)
    logger.propagate = False
    # Create a message format that matches RedactingFormatter
    formatter = RedactingFormatter(fields=list(PII_FIELDS))
    # Create a console handler
    handler = logging.StreamHandler()
    # Add our format to our handler
    handler.setFormatter(formatter)
    # Add our handler to our logger
    logger.addHandler(handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Function that creates the mysql connector using given
    credentials
    Returns:
        MySQLConnection object to a mysql database"""
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')
    mydb = mysql.connector.connect(
        host=host,
        user=username,
        password=password,
        database=db_name
    )
    return mydb


def main():
    """Function obtains a database connection, retrieves all rows
    under a filtered format like this"""
    logger = get_logger()
    connection = get_db()
    query = f'SELECT * FROM users;'

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        col_names = [i[0] for i in cursor.description]
        for row in rows:
            record = map(lambda x: f'{x[0]}={x[1]}', zip(col_names, row))
            message = f"{'; '.join(list(record))};"
            args = ("user_data", logging.INFO, None, None, message, None, None)
            log_record = logging.LogRecord(*args)
            logger.handle(log_record)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Formats a Log Record to remove the sensitive material
        out of the message block using filter_datum"""
        message = super().format(record)
        censored_txt = filter_datum(self.fields,
                                    self.REDACTION, message,
                                    self.SEPARATOR)
        return censored_txt


if __name__ == "__main__":
    main()
