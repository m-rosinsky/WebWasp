"""
file: src/command_timeout.py

This file contains the timeout command class.
"""

import argparse

from src.command_interface import CommandInterface

class CommandTimeout(CommandInterface):
    """
    This class handles the timeout command, which is
    used to get and set the timeout value for requests.
    """
    def __init__(self, name):
        super().__init__(name)

        # Create argument parser.
        self.parser = argparse.ArgumentParser(
            prog=self.name,
            description="Get/Set the timeout value for requests",
            add_help=False,
            epilog="Specify 0 for value to disable timeout"
        )

        # Add argparse args.
        self.parser.add_argument(
            'value',
            type=float,
            nargs='?',
            help="The timeout value in seconds"
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

        # Extract arguments.
        value = args.value

        if value is not None:
            value = round(value, 2)
            # If the value was provided, ensure it is positive
            if value <= 0:
                console.timeout_s = None
            else:
                console.timeout_s = value

        # Display the timeout value.
        print(f"Timeout -> {console.timeout_s}", end="")
        
        if console.timeout_s is not None:
            print(" seconds", end="")
        print("")

        return True

###   end of file   ###
