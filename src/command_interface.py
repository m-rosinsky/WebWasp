"""
file: src/command_interface.py

This file contains the command interface class, which outlines the
interface that all command classes must follow.
"""

class Command_Interface():
    def __init__(self, name):
        self.name = name

    """
    This class defines the interface for specific commands.
    """
    def get_usage(self):
        """
        This function prints the usage for the command.
        """
        print(f"Getting help for command: '{self.name}'\n")

    def run(self, parse):
        """
        This function runs the command given a parse of the arguments.

        This should return False if the console should exit after
        execution of the command.
        """
        pass

###   end of file   ###
