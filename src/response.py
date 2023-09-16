"""
file: src/response.py

This file contains the response class, which is used by the console
to store the most recent response.
"""

import http
import requests

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

    def print_summary(self):
        """
        This function prints a summary of the latest response, if one
        exists.
        """
        # If date_time is None, a response has not been generated.
        if not self.req:
            print("[🐝] No response captured")
            return

        print("[🐝] Summary of captured response:\n")

        # Print the response url.
        print("Response url:", end="\n   ")
        print(f"\033[36m{self.req.url}\033[0m")

        # Print date_time in mm/dd/yyyy   hh/mm/ss format.
        print("Response date/time:", end="\n   ")
        print(self.date_time.strftime("%m/%d/%Y   %H:%M:%S"))

        # Print the status code with color formatting.
        print("Status code:", end="\n   ")
        if self.req.status_code >= 200 and self.req.status_code < 300:
            print(f"\033[32m", end="")
        elif self.req.status_code >= 300 and self.req.status_code < 400:
            print(f"\033[33m", end="")
        elif self.req.status_code >= 400 and self.req.status_code < 500:
            print(f"\033[31m", end="")
        else:
            print(f"\033[0m", end="")
        print(f"{self.req.status_code} ", end="")

        http_code = http.HTTPStatus(self.req.status_code)
        print(f"\033[0m({http_code.phrase})")
    
    def print_cookies(self):
        """
        This function prints the cookies from the latest resposne
        to the console.
        """
        if not self.req:
            print("[🐝] No response captured")
            return
        
        print("[🐝] Response cookies:")

        for cookie, value in self.req.cookies.items():
            print(f"   {cookie}\t: {value}")

###   end of file   ###
