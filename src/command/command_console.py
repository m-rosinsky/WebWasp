"""
file: src/command_console.py

This file contains the console command class.
"""

import argparse
import os
import yaml

from src.logger import log
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

    def run(self, parse, console):
        super().run(parse)
        # Slice the command name off the parse so we only
        # parse the arguments.
        parse_trunc = parse[1:]

        # Match the subcommand.
        if len(parse_trunc) > 0:
            matched_subcmd = super()._get_cmd_match(
                parse_trunc[0],
                self.subparser.choices.keys(),
            )

            if matched_subcmd is not None:
                parse_trunc[0] = matched_subcmd

        try:
            args = self.parser.parse_args(parse_trunc)
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
        
        args.func(args, console)

        return True

    def _session_list(self, args, console):
        """
        Brief:
            This function lists all stored sessions.
        """
        log("Listing saved console sessions...", log_type='info')

        # Check that data file exists.
        if not os.path.exists(console.data_file):
            log("Persistent data file does not exist", log_type='error')
            return
        
        # Read the file data.
        file_data = ""
        try:
            with open(console.data_file, 'r', encoding='utf-8') as f:
                for line in f:
                    file_data += line
        except OSError:
            log("Unable to read persistent data file", log_type='error')
            return
        
        # Parse the file data as YAML.
        yaml_data = yaml.safe_load(file_data) or {}

        # Iterate through all top-level names.
        for name in yaml_data.keys():
            if name == 'cur_session':
                continue
            if name == console.cur_session:
                log(f"   \033[32m{name} *\033[0m")
            else:
                log(f"   {name}")

    def _session_reset(self, args, console):
        """
        Brief:
            This function clears all session data for the current session.
        """
        log(f"Resetting data for session '{console.cur_session}'", log_type='info')

        # Clear data.
        console.reset_data()

        # Update data.
        console.update_data()

###   end of file   ###
