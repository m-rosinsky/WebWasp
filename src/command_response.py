"""
file: src/command_response.py

This file contains the response command class.
"""

import argparse

from src.command_interface import CommandInterface

class CommandResponse(CommandInterface):
    """
    This class handles the response command, which is used
    to interact with the most recent response stored in the console.
    """
    def __init__(self, name):
        super().__init__(name)

        # Create argument parser.
        self.parser = argparse.ArgumentParser(
            prog=self.name,
            description="Show the data from the most recent response",
            add_help=False
        )

        # Add argparse args.
        self.parser.add_argument(
            '-t',
            action='store_true',
            help='Show response text'
        )
        self.parser.add_argument(
            '-e',
            nargs='?',
            const="default.txt",
            metavar="filepath",
            help='Export response to file (default: %(default)s)'
        )
        self.parser.add_argument(
            '-r',
            nargs='?',
            choices=['pdf','csv','txt'],
            const='txt',
            help='Generate a report of the response in a specified format (default .txt)'
        )

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

        print("Text: ", args.t)
        print("Export: ", args.e)
        print("Report: ", args.r)

        return True