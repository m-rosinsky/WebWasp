"""
file: src/command_clear.py

This file contains the clear command class.
"""

import os
import argparse

from src.context import Context
from src.node import CommandNode
from src.command.command_interface import CommandInterface

class CommandClear(CommandInterface):
    """
    This class handles the clear command, which clears the screen.
    """
    def __init__(self, name):
        super().__init__(name)

        # Create argument parser.
        self.parser = argparse.ArgumentParser(
            prog=self.name,
            description='Clear the screen',
            add_help=False
        )
        super().add_help(self.parser)

    def run(self, parse: list, context: Context, cmd_tree: CommandNode) -> bool:
        # Resolve command shortening.
        parse = super()._resolve_parse(self.name, parse, cmd_tree)

        if parse is None:
            return True

        # Parse arguments.
        try:
            _args = self.parser.parse_args(parse)
        except argparse.ArgumentError:
            self.parser.print_help()
            return True
        except SystemExit:
            # Don't let argparse exit the program.
            return True

        # Clear the screen with OS call.
        os.system('cls' if os.name == 'nt' else 'clear')
        return True

###   end of file   ###
