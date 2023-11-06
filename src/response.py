"""
file: src/response.py

This file contains the response class, which is used by the console
to store the most recent response.
"""

import http
import requests

from src.logger import log

class Response:
    """
    This class contains the information from the most recent response.

    Members:
    resp_date - The date the response was collected.
    resp_time - The time the response was collected.

    status_code - The HTTP status code
    text - The literal text of the response (source code)
    """
    def __init__(self):
        # Date/time details.
        self.date_time = None

        # The requests object response.
        self.req = None

        # The POST data.
        self.post_data = None

    def print_summary(self):
        """
        This function prints a summary of the latest response, if one
        exists.
        """
        # Check if we are missing a response.
        if not self.req:
            log("No response captured", log_type='warning')
            return

        log("Summary of captured response:\n", log_type='info')

        # Print the response url.
        log("Response url:", end="\n   ")
        log(f"\033[36m{self.req.url}\033[0m")

        # Print date_time in mm/dd/yyyy   hh/mm/ss format.
        log("Response date/time:", end="\n   ")
        log(self.date_time.strftime("%m/%d/%Y   %H:%M:%S"))

        # Print the status code with color formatting.
        log("Status code:", end="\n   ")
        if self.req.status_code >= 200 and self.req.status_code < 300:
            log(f"\033[32m", end="")
        elif self.req.status_code >= 300 and self.req.status_code < 400:
            log(f"\033[33m", end="")
        elif self.req.status_code >= 400 and self.req.status_code < 500:
            log(f"\033[31m", end="")
        else:
            log(f"\033[0m", end="")
        log(f"{self.req.status_code} ", end="")

        http_code = http.HTTPStatus(self.req.status_code)
        log(f"\033[0m({http_code.phrase})")

        if self.post_data is not None:
            log(f"POST parameters:")
            for name, value in self.post_data.items():
                log(f"   '{name}' : '{value}'")
    
    def print_cookies(self):
        """
        This function prints the cookies from the latest resposne
        to the console.
        """
        if not self.req:
            log("No response captured", log_type='warning')
            return
        
        log("Response cookies:", log_type='info')

        for cookie, value in self.req.cookies.items():
            log(f"   {cookie}\t: {value}")

###   end of file   ###
