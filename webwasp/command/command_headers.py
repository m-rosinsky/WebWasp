"""
file: src/command_headers.py

This file contains the headers command class.
"""

import argparse

from webwasp.logger import log
from webwasp.context import Context
from webwasp.node import CommandNode
from webwasp.headers import Headers
from webwasp.command.command_interface import CommandInterface

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

    def create_cmd_tree(self) -> CommandNode:
        root = super().create_cmd_tree()

        # Special command additions here to add the
        # header fields to the 'set' and 'unset' commands.
        if root is None:
            return root
        
        h = Headers()
        for child in root.children:
            if child.name in ["set", "unset"]:
                for field in h.fields:
                    node = CommandNode(field)
                    child.children.append(node)
                for auth in h.auth:
                    node = CommandNode(auth)
                    child.children.append(node)

        return root

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

        # If no subcommand was specified, show list.
        if not hasattr(args, 'func'):
            self._list(context)
            return True

        args.func(args, context)
        context.save_data()

        return True

    def _list(self, context: Context):
        """
        This function lists all headers currently stored.
        """
        log("Current header fields:", log_type='info')
        context.headers.print_fields()

    def _set(self, args: argparse.Namespace, context: Context):
        """
        This function sets a header field to a specified value.
        """
        if not context.headers.field_valid(args.field):
            log(f"Invalid header field: '{args.field}'", log_type='error')
            log("Run 'headers' to see list of valid fields")
            return

        context.headers.set_field(args.field, args.value)
        log(
            f"Set header field:\n   {args.field} : '{args.value}'",
            log_type='info',
        )

    def _unset(self, args: argparse.Namespace, context: Context):
        """
        This function unsets a header field.
        """
        if not context.headers.field_valid(args.field):
            log(f"Invalid header field: '{args.field}'", log_type='error')
            log("Run 'headers' to see list of valid fields")
            return

        context.headers.set_field(args.field, None)
        log(f"Unset header field:\n   {args.field}", log_type='info')

    def _clear(self, args: argparse.Namespace, context: Context):
        """
        This function unsets all header fields.
        """
        context.headers.clear_fields()
        log("Cleared all header fields", log_type='info')

###   end of file   ###
