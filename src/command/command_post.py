"""
file: src/command_post.py

This file contains the post command class.
"""

import argparse
import datetime
import http
import requests

from src.logger import log
from src.command.command_interface import CommandInterface

class CommandPost(CommandInterface):
    """
    This class handles the post command, which sends
    HTTP POST requests to a url/server.
    """
    def __init__(self, name):
        super().__init__(name)

        # Create argument parser and help.
        self.parser = argparse.ArgumentParser(
            prog=self.name,
            description='Send an HTTP POST request to a server/url',
            add_help=False,
        )
        super().add_help(self.parser)

        # Add argparse args.
        self.parser.add_argument(
            'url',
            type=str,
            help='The url to make a request to',
        )
        self.parser.add_argument(
            'params',
            nargs='*',
            default=[],
            help='Parameters from params to send with post request',
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
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://' + url

        # Prepare the parameters.
        data = {}
        for param in args.params:
            if not param in console.params:
                log(f"Parameter {param} not in params list", log_type='error')
                return True
            data[param] = console.params[param]

        # Construct the headers dictionary with only fields are are not None
        # in the console's headers object.
        headers = {}
        for field, value in console.headers.fields.items():
            if value is not None:
                headers[field] = value

        # Construct the auth dictionary.
        auth = None
        if console.headers.auth['auth-user'] is not None:
            auth = (console.headers.auth['auth-user'], console.headers.auth['auth-pass'])

        log(
            f"Sending POST request to \033[36m{url}\033[0m...",
            log_type='info',
        )
        log(f"POST request made with parameters:")
        for name, value in data.items():
            log(f"   '{name}' : '{value}'")

        # Perform the POST request.
        req = None
        try:
            req = requests.post(
                url,
                data=data,
                timeout=console.timeout_s,
                auth=auth,
                headers=headers,
                cookies=console.cookies,
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
        log("POST request completed. Status code: ", log_type='info', end='')

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
        console.response.req_text = req.text
        console.response.post_data = data

        # Set the console flag to indicate a response has been captured,
        # and report.
        console.has_response = True
        log(
            "Response captured! Type 'response show' for summary",
            log_type='info',
        )

        return True

###   end of file   ###
