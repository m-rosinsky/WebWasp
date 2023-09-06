"""
file: src/command_get.py

This file contains the get command class.
"""

import http
import requests
import argparse
import datetime

from src.command_interface import CommandInterface

class CommandGet(CommandInterface):
    """
    This class handles the get command, which sends
    HTTP 1.1 GET requests to a url/server.
    """
    def __init__(self, name):
        super().__init__(name)

        # Create argument parser.
        self.parser = argparse.ArgumentParser(
            prog=self.name,
            description="Send an HTTP 1.1 GET request to a server/url",
            add_help=False
        )

        # Add argparse args.
        self.parser.add_argument(
            'url',
            type=str,
            help="The url to make a request to")

    def get_help(self):
        super().get_help()

    def run(self, parse, console):
        super().run(parse)
        # Slice the command name off the parse so we only
        # parse the arguments.
        parse_trunc = parse[1:]

        try:
            args = self.parser.parse_args(parse_trunc)
        except argparse.ArgumentError:
            self.get_help()
            return True
        except SystemExit:
            # Don't let argparse exit the program.
            return True

        # Extract arguments.
        url = args.url

        # Add "http://" onto from of URL if no scheme is supplied.
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url

        # Inform the user the full URL.
        print(f"[🐝] Sending GET request to \033[36m{url}\033[0m...")

        # Perform get request from request lib.
        req = None
        try:
            req = requests.get(
                url,
                timeout=console.timeout_s
            )
        except requests.exceptions.RequestException as req_ex:
            print(f"{req_ex}")
            return True
        except KeyboardInterrupt:
            print("^C")
            if req:
                req.close()
            return True

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

        # Save the response fields to the console.
        console.response.date_time = datetime.datetime.now()
        console.response.status_code = req.status_code
        console.response.text = req.text

        # Set the console flag to indicate a response has been captured,
        # and report.
        console.has_response = True
        print("[🐝] Response captured! Use 'response' command for details")

        return True

###   end of file   ###
