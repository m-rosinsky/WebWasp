"""
File:
    src/context.py

Brief:
    This file contains the context class.
"""

from src.response import Response
from src.headers import Headers

# The default request timeout value in seconds.
DEFAULT_TIMEOUT = 2.0

# The default name for a session.
DEFAULT_SESSION_NAME = 'default'

class Context:
    """
    Brief:
        This class contains a context for the current WebWasp session.
    """
    def __init__(self):
        # The current session name.
        self.cur_session = DEFAULT_SESSION_NAME
        
        # The request timeout value.
        self.timeout = DEFAULT_TIMEOUT

        # This class holds the most recent response information.
        self.response = Response()
        self.has_response = False

        # This holds the request headers.
        self.headers = Headers()

        # This holds the console variables.
        self.vars = {}

        # This holds the request parameters.
        self.params = {}

        # This holds the request cookies.
        self.cookies = {}


###   end of file   ###
