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

        if not console.has_response:
            print("[🐝] No response captured")
            return True

        # If the -t option is specified, only print the text.
        # Otherwise, print the response summary.
        if args.t:
            print(console.response.text)
        elif not args.e and not args.r:
            console.response.print_summary()
            print("\n[🐝] Re-run with '-t' flag to show response text")

        return True

###   end of file   ###
