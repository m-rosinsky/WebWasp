"""
file: src/command_interface.py

This file contains the command interface class, which outlines the
interface that all command classes must follow.
"""

import argparse
from abc import ABC, abstractmethod

from webwasp.logger import log
from webwasp.context import Context
from webwasp.node import CommandNode

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
    def run(self, parse: list, context: Context, cmd_tree: CommandNode) -> bool:
        """
        This function runs the command given a parse of the arguments.

        It is also supplied a reference to the context instance so it
        can make edits.

        This should return False if the program should exit after
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

    def _resolve_parse(self, name: str, parse: list, cmd_tree: CommandNode) -> list:
        """
        Brief:
            This function resolves command shortening by comparing the
            class's command tree to the provided command parse.

        Arguments:
            name: str
                The name of the base command

            parse: list
                The command parse, without the base command

            cmd_tree: CommandNode
                The root node of the command tree.
        """
        res_parse = parse

        # Find the root node of the base command provided in the name param.
        base_node = None
        for node in cmd_tree.children:
            if node.name == name:
                base_node = node
                break

        # If not found, return.
        if base_node is None:
            return res_parse
        
        # Find matches for each token in the parse.
        cur_node = base_node
        parse_index = 0
        for token in parse:
            matches = [c for c in cur_node.children if c.name.startswith(token)]

            # If no matches, return. When these arguments are parsed
            # the help message will be displayed.
            if not matches:
                return res_parse
            
            # If ambiguous matches, print possibilities.
            if len(matches) > 1:
                log(f"Ambiguous argument: '{token}'. Potential matches:", log_type='error')
                for m in matches:
                    log(f"   {m.name}")
                return None
            
            # Perform resolution with only match.
            parse[parse_index] = matches[0].name

            # Increment index and current node.
            parse_index += 1
            cur_node = matches[0]

        # Return the resolved parse list.
        return res_parse

###   end of file   ###
