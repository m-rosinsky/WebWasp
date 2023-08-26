"""
file: src/command_interface.py

This file contains the command interface class, which outlines the
interface that all command classes must follow.
"""

from abc import ABC, abstractmethod

class CommandInterface(ABC):
    """
    This class is the command interface for all other command classes.

    It should not be directly instantiated.

    Members:
    name - The name of the command for usage display.
    """
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def get_help(self):
        """
        This function prints the help message for the command.
        """
        print(f"Getting help for command: '{self.name}'...\n")

    @abstractmethod
    def get_usage(self):
        """
        This function prints the usage for the command.
        """
        print("Usage: ", end="")

    @abstractmethod
    def run(self, parse, console=None):
        """
        This function runs the command given a parse of the arguments.

        It is also supplied a reference to the console instance so it
        can make edits.

        This should return False if the console should exit after
        execution of the command.
        """
        return

###   end of file   ###
