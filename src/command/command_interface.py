"""
file: src/command_interface.py

This file contains the command interface class, which outlines the
interface that all command classes must follow.
"""

import argparse
from abc import ABC, abstractmethod

from src.logger import log
from src.node import CommandNode

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
            '-h',
            '--help',
            action='help',
            default=argparse.SUPPRESS,
            help='Show this help message',
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
    
    def create_cmd_tree(self) -> CommandNode:
        """
        Brief:
            This function creates the command syntax tree for the command.
        
        Return:
            CommandNode
                A node with the root being the top-level command.
        """
        return self._cmd_tree_recurse(self.name, self.parser)
    
    def _cmd_tree_recurse(self, name: str, parser: argparse.ArgumentParser) -> CommandNode:
        """
        Brief:
            This is a helper function to recurse through parsers.
        """
        node = CommandNode(name)

        if parser is None:
            return node
        
        # These are private members that technically should not be accessed,
        # which means they may be changed in future updates of argparse.
        # SPECIAL ATTENTION SHOULD BE PAID in udpates, or argparse
        # version should be enforced.
        sp = parser._subparsers
        if sp is None:
            return node
        
        choices = sp._actions[1].choices
        if choices is None:
            return node
        
        for child_name, child_parser in choices.items():
            child_node = self._cmd_tree_recurse(child_name, child_parser)
            node.children.append(child_node)

        return node

    def _get_cmd_match(self, cmd, l):
        """
        Brief:
            This function attempts to match the entered command with
            the closest fit in the subparser.

        Arguments:
            cmd: str
                The subcommand entered by the user.

            l: list
                The list of possible commands.
        """
        matches = [c for c in l if c.startswith(cmd)]

        if len(matches) == 1:
            return matches[0]
        
        # If the list comprehension returned multiple values, then the command
        # was ambiguous.
        if len(matches) > 1:
            log(f"Ambiguous command: '{cmd}'. Potential matches:", log_type='error')
            for match in matches:
                log(f"   {match}")
            return None
        
        # No matches were returned, so the command was invalid.
        return None

###   end of file   ###
