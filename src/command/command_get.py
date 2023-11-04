"""
file: src/command_get.py

This file contains the get command class.
"""

import http
import argparse
import datetime
import requests

from src.command.command_interface import CommandInterface

class CommandGet(CommandInterface):
    """
    This class handles the get command, which sends
    HTTP 1.1 GET requests to a url/server.
    """
    def __init__(self, name):
        super().__init__(name)

        # Create argument parser and help.
        self.parser = argparse.ArgumentParser(
            prog=self.name,
            description="Send an HTTP 1.1 GET request to a server/url",
            add_help=False
        )
        super().add_help(self.parser)

        # Add argparse args.
        self.parser.add_argument(
            "url",
            type=str,
            help="The url to make a request to"
        )
        self.parser.add_argument(
            "--no-params",
            action="store_true",
            help="Perform request without stored parameters in url"
        )
        self.parser.add_argument(
            "--no-cookies",
            action="store_true",
            help="Perform request without stored cookies"
        )

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

        # If the --no-params flag was specified, unset params.
        params = console.params
        if args.no_params:
            params = {}

        # Prepare the full URL.
        prep = requests.Request("GET", url, params=params).prepare()

        # If the --no-cookies flag was specified, unset cookies.
        cookies = console.cookies
        if args.no_cookies:
            cookies = {}

        # Inform the user the full URL.
        print(f"[🐝] Sending GET request to \033[36m{prep.url}\033[0m...")

        # Construct the headers dictionary with only fields are are not None
        # in the console's headers object.
        headers = {}
        for field, value in console.headers.fields.items():
            if value is not None:
                headers[field] = value

        # Construct the auth dictionary.
        auth = None
        if console.headers.auth["auth-user"] is not None:
            auth = (console.headers.auth["auth-user"], console.headers.auth["auth-pass"])

        # Perform get request from request lib.
        req = None
        try:
            req = requests.get(
                prep.url,
                timeout=console.timeout_s,
                auth=auth,
                headers=headers,
                cookies=cookies,
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
        print("[🐝] GET request completed. Status code: ", end="")

        if req.status_code >= 200 and req.status_code < 300:
            print("\033[32m", end="")
        elif req.status_code >= 300 and req.status_code < 400:
            print("\033[33m", end="")
        elif req.status_code >= 400 and req.status_code < 500:
            print("\033[31m", end="")
        else:
            print("\033[0m", end="")
        print(f"{req.status_code} ", end="")

        http_code = http.HTTPStatus(req.status_code)
        print(f"\033[0m({http_code.phrase})")

        # Save the response fields to the console.
        console.response.date_time = datetime.datetime.now()
        console.response.req = req

        # Set the console flag to indicate a response has been captured,
        # and report.
        console.has_response = True
        print("[🐝] Response captured! Type 'response show' for summary")

        return True

###   end of file   ###