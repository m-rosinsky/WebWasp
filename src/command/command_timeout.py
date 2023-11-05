"""
file: src/command_timeout.py

This file contains the timeout command class.
"""

import argparse

from src.logger import log
from src.command.command_interface import CommandInterface

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
            description='Get/Set the timeout value for requests',
            add_help=False,
            epilog='Specify 0 for value to disable timeout'
        )
        super().add_help(self.parser)

        # Add argparse args.
        self.parser.add_argument(
            'value',
            type=float,
            nargs='?',
            help='The timeout value in seconds'
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
        value = args.value

        if value is not None:
            value = round(value, 2)
            # If the value was provided, ensure it is positive
            if value <= 0:
                console.timeout_s = None
            else:
                console.timeout_s = value

        # Display the timeout value.
        log(f"Timeout -> {console.timeout_s}", log_type='info', end="")
        
        if console.timeout_s is not None:
            log(" seconds", end="")
        log("")

        return True

###   end of file   ###
