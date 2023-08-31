"""
file: src/response.py

This file contains the response class, which is used by the console
to store the most recent response.
"""

class Response:
    """
    This class contains the information from the most recent response.

    Members:
    status_code - The HTTP status code
    text - The literal text of the response (source code)
    """
    def __init__(self):
        self.status_code = 0
        self.text = ""

###   end of file   ###
