"""
    exceptions.py

    Exceptions raised by the Axis Direct REST API client.

    :copyright: (c) 2024 Abhay Braja.
    :license: see LICENSE for details.
"""


class AxisDAPIException(Exception):
    """
    Base exception class representing a Axis Direct client exception.

    - `.code` (HTTP error code) and `.message` (error text).
    """

    def __init__(self, message, code=500):
        """Initialize the exception."""
        super(AxisDAPIException, self).__init__(message)
        self.code = code


class GeneralException(AxisDAPIException):
    """An unclassified, general error. Default code is 500."""

    def __init__(self, message, code=500):
        """Initialize the exception."""
        super(GeneralException, self).__init__(message, code)


class TokenException(AxisDAPIException):
    """Represents all token and authentication related errors. Default code is 403."""

    def __init__(self, message, code=403):
        """Initialize the exception."""
        super(TokenException, self).__init__(message, code)


class DataException(AxisDAPIException):
    """Represents a bad response from the backend Order Management System (OMS). Default code is 502."""

    def __init__(self, message, code=502):
        """Initialize the exception."""
        super(DataException, self).__init__(message, code)
