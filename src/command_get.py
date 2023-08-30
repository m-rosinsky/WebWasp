"""
file: src/command_get.py

This file contains the get command class.
"""

import http
import requests

from src.command_interface import CommandInterface

class CommandGet(CommandInterface):
    """
    This class handles the get command, which sends
    HTTP 1.1 GET requests to a url/server.
    """
    def __init__(self, name):
        super().__init__(name)

    def get_help(self):
        super().get_help()
        print("Description:")
        print("  Send an HTTP 1.1 GET request to a server/url")
        print("")
        self.get_usage()

    def get_usage(self):
        super().get_usage()
        print("get url\n")

        print("Arguments:")
        print("  url - The url to perform a GET request")

    def run(self, parse, console=None):
        """
        This function executes the get command.

        Check interface docs for args and return vals.
        """
        super().run(parse)

        # Ensure console exists.
        if not console:
            print("[🛑] Error: Missing console context in get call")
            return False

        # Check usage.
        parse_len = len(parse)
        if parse_len != 2:
            print("[🛑] Error: Invalid number of arguments\n")
            self.get_usage()
            return True

        # Add "http://" onto from of URL if no scheme is supplied.
        url = parse[1]
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url

        # Inform the user the full URL.
        print(f"[🐝] Sending GET request to {url}...")

        # Perform get request from request lib.
        req = None
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException as req_ex:
            print(f"{req_ex}")
            return True
        except KeyboardInterrupt:
            print("^C")
            if req:
                req.close()
            return True

        # Save fields in console members.
        console.http_status = req.status_code

        # Print the status code.
        print(f"[🐝] GET request completed. Status code: ", end="")

        if req.status_code >= 200 and req.status_code < 300:
            print(f"\033[32m", end="")
        elif req.status_code >= 300 and req.status_code < 400:
            print(f"\033[33m", end="")
        elif req.status_code >= 400 and req.status_code < 500:
            print(f"\033[31m", end="")
        else:
            print(f"\033[0m", end="")
        print(f"{req.status_code} ", end="")

        http_code = http.HTTPStatus(req.status_code)
        print(f"\033[0m({http_code.phrase})")

        return True

###   end of file   ###
