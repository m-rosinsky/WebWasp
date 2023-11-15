"""
file: src/command_console.py

This file contains the console command class.
"""

import argparse

from src.logger import log
from src.context import *
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

        # Create the console session load subparser.
        self.parser_session_load = self.session_subparser.add_parser(
            'load',
            description='Load an existing session',
            help='Load an existing session',
            add_help=False,
        )
        self.parser_session_load.set_defaults(func=self._session_load)
        super().add_help(self.parser_session_load)
        self.parser_session_load.add_argument(
            'name',
            type=str,
            help='The name of the session',
        )

        # Create the console session copy subparser.
        self.parser_session_copy = self.session_subparser.add_parser(
            'copy',
            description='Copy data from the current session into [name] and switch to it',
            help='Copy data from the current session into [name] and switch to it',
            add_help=False,
        )
        self.parser_session_copy.set_defaults(func=self._session_copy)
        super().add_help(self.parser_session_copy)
        self.parser_session_copy.add_argument(
            'name',
            type=str,
            help='The name of the session',
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

    def _session_list(self, args: argparse.Namespace, context: Context):
        """
        Brief:
            This function lists all stored sessions.
        """
        log(f"Console session list:", log_type='info')
        
        try:
            context.print_session_list()
        except DataError:
            log("Failed to retreive session list", log_type='error')

    def _session_reset(self, args: argparse.Namespace, context: Context):
        """
        Brief:
            This function clears all session data for the current session.
        """
        log(f"Resetting data for session '{context.cur_session}'", log_type='info')
        try:
            context.reset_data()
        except DataError:
            log("Failed to write to persistent file", log_type='error')

    def _session_new(self, args: argparse.Namespace, context: Context):
        """
        Brief:
            This function creates a new session with blank data.
        """
        # Add new session.
        try:
            context.new_session(args.name)
        except DupSessionError:
            log(f"Session with name '{args.name}' already exists", log_type='error')
            return
        except DataError:
            log("Unable to write to persistent data file", log_type='error')
            return
        
        log(f"Created and switched to new session: '{args.name}'", log_type='info')
    
    def _session_load(self, args: argparse.Namespace, context: Context):
        """
        Brief:
            This function loads an existing session.
        """
        try:
            context.load_session(args.name)
        except SessionNotFoundError:
            log(f"Session '{args.name}' does not exist", log_type='error')
            return
        except DataError:
            log("Unable to read from persistent data file", log_type='error')
            return
        
        log(f"Switched to session '{args.name}'", log_type='info')

    def _session_copy(self, args: argparse.Namespace, context: Context):
        """
        Brief:
            This function copies an existing session.
        """
        orig_name = context.cur_session
        try:
            context.copy_session(args.name)
        except DataError:
            log("Unable to read from persistent data file", log_type='error')
            return
        
        log(f"Copied data from session '{orig_name}' to '{args.name}'", log_type='info')
        log(f"Switched to session '{args.name}'", log_type='info')

###   end of file   ###
