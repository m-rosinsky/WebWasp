"""
file: src/response.py

This file contains the response class, which is used by the console
to store the most recent response.
"""

import http

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

        self.status_code = 0
        self.text = ""

    def print_summary(self):
        """
        This function prints a summary of the latest response, if one
        exists.
        """
        # If date_time is None, a response has not been generated.
        if not self.date_time:
            print("[🐝] No response captured")
            return

        print("[🐝] Summary of captured response:\n")

        # Print date_time in mm/dd/yyyy   hh/mm/ss format.
        print("Response date/time:", end="\n   ")
        print(self.date_time.strftime("%m/%d/%Y   %H:%M:%S"))

        # Print the status code with color formatting.
        print("Status code:", end="\n   ")
        if self.status_code >= 200 and self.status_code < 300:
            print(f"\033[32m", end="")
        elif self.status_code >= 300 and self.status_code < 400:
            print(f"\033[33m", end="")
        elif self.status_code >= 400 and self.status_code < 500:
            print(f"\033[31m", end="")
        else:
            print(f"\033[0m", end="")
        print(f"{self.status_code} ", end="")

        http_code = http.HTTPStatus(self.status_code)
        print(f"\033[0m({http_code.phrase})")

###   end of file   ###
