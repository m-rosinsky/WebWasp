"""
file: src/command_help.py

This file contains the help command class definition.
"""

from src.command_interface import Command_Interface

class Command_Help(Command_Interface):
    def __init__(self, name):
        super().__init__(name)

    def get_usage(self):
        super().get_usage()
        print("Description:")
        print("Get general help, or help for a specified command\n")

        print("Usage:")
        print("help [cmd]\n")

    def run(self, parse):
        super().run(parse)

        parse_len = len(parse)
        # Check usage.
        if parse_len > 2:
            print("Error: Extra arguments\n")
            self.get_usage()
            return True

        # If command is specified, ensure it exists.
        if parse_len == 2:
            print(f"Got specified command: '{parse[1]}'")
            return True

        # Get generalized help.
        print("Getting general help...")
        return True

###   end of file   ###
