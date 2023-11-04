"""
file: src/command_interface.py

This file contains the command interface class, which outlines the
interface that all command classes must follow.
"""

import argparse
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
        self.parser = None

    def add_help(self, parser):
        parser.add_argument(
            "-h",
            "--help",
            action="help",
            default=argparse.SUPPRESS,
            help="show this help message"
        )

    @abstractmethod
    def run(self, parse, console=None):
        """
        This function runs the command given a parse of the arguments.

        It is also supplied a reference to the console instance so it
        can make edits.

        This should return False if the console should exit after
        execution of the command.
        """
        return True

###   end of file   ###
