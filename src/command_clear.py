"""
file: src/command_clear.py

This file contains the clear command class.
"""

import os

from src.command_interface import CommandInterface

class CommandClear(CommandInterface):
    """
    This class handles the clear command, which clears the screen.
    """
    def __init__(self, name):
        super().__init__(name)

    def get_help(self):
        super().get_help()
        print("Description:")
        print("  Clear the terminal\n")
        self.get_usage()

    def get_usage(self):
        super().get_usage()
        print("clear\n")

    def run(self, parse, console=None):
        super().run(parse)

        parse_len = len(parse)
        # Check usage.
        if parse_len != 1:
            print("[🛑] Error: Extra arguments\n")
            self.get_usage()
            return True

        # Clear the screen with OS call.
        os.system('cls' if os.name == 'nt' else 'clear')
        return True

###   end of file   ###
