"""
file: src/command_headers.py

This file contains the headers command class.
"""

import argparse

from src.logger import log
from src.command.command_interface import CommandInterface

class CommandHeaders(CommandInterface):
    """
    This class handles the headers command, which is used
    to set and unset different HTTP 1.1 header values.

    The specific header fields that can be set/unset are
    hardcoded, and if an improper selection is made, an error
    is returned.
    """
    def __init__(self, name):
        super().__init__(name)

        # Create argument parser and help.
        self.parser = argparse.ArgumentParser(
            prog=self.name,
            description='Set and unset custom HTTP 1.1 headers',
            add_help=False
        )
        super().add_help(self.parser)

        # Create the subparser object.
        self.subparser = self.parser.add_subparsers()

        # Create the headers set command subparser.
        self.parser_set = self.subparser.add_parser(
            'set',
            description='Set the value for a header field',
            help='Set the value for a header field',
            add_help=False
        )
        super().add_help(self.parser_set)
        self.parser_set.set_defaults(func=self._set)
        self.parser_set.add_argument(
            'field',
            type=str,
            help='The header field to set'
        )
        self.parser_set.add_argument(
            'value',
            type=str,
            help='The header field value'
        )

        # Create the headers unset command subparser.
        self.parser_unset = self.subparser.add_parser(
            'unset',
            description='Unset the value for a header field',
            help='Unset the value for a header field',
            add_help=False
        )
        super().add_help(self.parser_unset)
        self.parser_unset.set_defaults(func=self._unset)
        self.parser_unset.add_argument(
            'field',
            type=str,
            help='The header field to unset'
        )

        # Create the headers clear command subparser.
        self.parser_clear = self.subparser.add_parser(
            'clear',
            description='Unset all header field values',
            help='Unset all header field values',
            add_help=False
        )
        super().add_help(self.parser_clear)
        self.parser_clear.set_defaults(func=self._clear)

    def run(self, parse, console):
        super().run(parse)
        # Slice the command name off the parse so we only
        # parse the arguments.
        parse_trunc = parse[1:]

        try:
            args = self.parser.parse_args(parse_trunc)
        except argparse.ArgumentError:
            self.parser.print_help()
            return True
        except SystemExit:
            # Don't let argparse exit the program.
            return True

        # If no subcommand was specified, show list.
        if not hasattr(args, 'func'):
            self._list(console)
            return True

        args.func(args, console)
        console.update_data()

        return True

    def _list(self, console):
        """
        This function lists all headers currently stored.
        """
        log("Current header fields:", log_type='info')
        console.headers.print_fields()

    def _set(self, args, console):
        """
        This function sets a header field to a specified value.
        """
        if not console.headers.field_valid(args.field):
            log(f"Invalid header field: '{args.field}'", log_type='error')
            log("Run 'headers' to see list of valid fields")
            return

        console.headers.set_field(args.field, args.value)
        log(
            f"Set header field:\n   {args.field} : '{args.value}'",
            log_type='info',
        )

    def _unset(self, args, console):
        """
        This function unsets a header field.
        """
        if not console.headers.field_valid(args.field):
            log(f"Invalid header field: '{args.field}'", log_type='error')
            log("Run 'headers' to see list of valid fields")
            return

        console.headers.set_field(args.field, None)
        log(f"Unset header field:\n   {args.field}", log_type='info')

    def _clear(self, args, console):
        """
        This function unsets all header fields.
        """
        console.headers.clear_fields()
        log("Cleared all header fields", log_type='info')

###   end of file   ###
