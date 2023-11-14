"""
file: src/command_console.py

This file contains the console command class.
"""

import argparse
import os
import yaml

from src.logger import log
from src.context import Context
from src.node import CommandNode
from src.command.command_interface import CommandInterface

class CommandConsole(CommandInterface):
    """
    This class handles the console command, which is used
    to modify console settings and session data.
    """
    def __init__(self, name):
        super().__init__(name)

        # Create argument parser and help.
        self.parser = argparse.ArgumentParser(
            prog=self.name,
            description='Modify console settings and session data',
            add_help=False,
        )
        super().add_help(self.parser)

        # Create the subparser object.
        self.subparser = self.parser.add_subparsers()

        # Create the console session command subparser.
        self.parser_session = self.subparser.add_parser(
            'session',
            description='Modify session data',
            help='Modify session data',
            add_help=False
        )
        super().add_help(self.parser_session)

        # Create the session subparser.
        self.session_subparser = self.parser_session.add_subparsers()

        # Create the console session list subparser.
        self.parser_session_list = self.session_subparser.add_parser(
            'list',
            description='List all stored sessions',
            help='List all stored sessions',
            add_help=False,
        )
        self.parser_session_list.set_defaults(func=self._session_list)
        super().add_help(self.parser_session_list)

        # Create the console session reset subparser.
        self.parser_session_reset = self.session_subparser.add_parser(
            'reset',
            description='Reset all data in the current session',
            help='Reset all data in the current session',
            add_help=False,
        )
        self.parser_session_reset.set_defaults(func=self._session_reset)
        super().add_help(self.parser_session_reset)

        # Create the console session new subparser.
        self.parser_session_new = self.session_subparser.add_parser(
            'new',
            description='Create a new session with blank data',
            help='Create a new session with blank data',
            add_help=False,
        )
        self.parser_session_new.set_defaults(func=self._session_new)
        super().add_help(self.parser_session_new)
        self.parser_session_new.add_argument(
            'name',
            type=str,
            help='The name for the new session',
        )

    def run(self, parse: list, context: Context, cmd_tree: CommandNode) -> bool:
        # Resolve command shortening.
        parse = super()._resolve_parse(self.name, parse, cmd_tree)

        if parse is None:
            return True

        # Parse arguments.
        try:
            args = self.parser.parse_args(parse)
        except argparse.ArgumentError:
            self.parser.print_help()
            return True
        except SystemExit:
            # Don't let argparse exit the program.
            return True

        # If no subcommand was specified, show help.
        if not hasattr(args, 'func'):
            self.parser.print_help()
            return True
        
        args.func(args, context)

        return True

    def _session_list(self, args: argparse.Namespace, context: Context) -> bool:
        """
        Brief:
            This function lists all stored sessions.
        """
        log(f"Console session list:", log_type='info')
        if context is None:
            return True
        
        context.print_session_list()
        return True

    def _session_reset(self, args: argparse.Namespace, context: Context) -> bool:
        """
        Brief:
            This function clears all session data for the current session.
        """
        log(f"Resetting data for session '{context.cur_session}'", log_type='info')
        context.reset_data()
        return True

    def _session_new(self, args: argparse.Namespace, context: Context) -> bool:
        """
        Brief:
            This function creates a new session with blank data.
        """
        # Add new session. If this returned False, the session already exists.
        if not context.new_session(args.name):
            log(f"Session with name '{args.name}' already exists", log_type='error')
            return True
        
        log(f"Created and switched to new session: '{args.name}'", log_type='info')
        return True

###   end of file   ###
