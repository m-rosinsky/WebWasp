"""
file: src/command_cookies.py

This file contains the cookies command class.
"""

import argparse

from webwasp.logger import log
from webwasp.context import Context
from webwasp.node import CommandNode
from webwasp.command.command_interface import CommandInterface

class CommandCookies(CommandInterface):
    """
    This class handles the cookies command, which is used
    to set and unset cookie values passed in requests.
    """
    def __init__(self, name):
        super().__init__(name)

        # Create argument parser and help.
        self.parser = argparse.ArgumentParser(
            prog=self.name,
            description='Modify the cookies for requests',
            add_help=False
        )
        super().add_help(self.parser)

        # Create the subparser object.
        self.subparser = self.parser.add_subparsers()

        # Create the cookies add command subparser.
        self.parser_add = self.subparser.add_parser(
            'add',
            description='Add a cookie',
            help='Add a cookie',
            add_help=False
        )
        self.parser_add.set_defaults(func=self._add)
        self.parser_add.add_argument(
            'name',
            type=str,
            help='The name of the new cookie'
        )
        self.parser_add.add_argument(
            'value',
            type=str,
            help='The value of the new cookie'
        )

        # Create the params remove command subparser.
        self.parser_remove = self.subparser.add_parser(
            'remove',
            description='Remove a cookie',
            help='Remove a cookie',
            add_help=False
        )
        self.parser_remove.set_defaults(func=self._remove)
        self.parser_remove.add_argument(
            'name',
            type=str,
            help='The name of the cookie to remove'
        )

        # Create the params clear command subparser.
        self.parser_clear = self.subparser.add_parser(
            'clear',
            description='Remove all cookies',
            help='Remove all cookies',
            add_help=False
        )
        self.parser_clear.set_defaults(func=self._clear)

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
        This function lists all cookies currently stored.
        """
        log("Current stored cookies:", log_type='cookie')
        for name, value in context.cookies.items():
            print(f"   '{name}' : '{value}'")

    def _add(self, args: argparse.Namespace, context: Context):
        """
        This function adds a new cookie.
        """
        context.cookies[args.name] = args.value
        log("Added cookie:", log_type='cookie')
        log(f"   '{args.name}' : '{args.value}'")

    def _remove(self, args: argparse.Namespace, context: Context):
        """
        This function removes a cookie.
        """
        if args.name not in context.cookies:
            log(f"Unknown cookie: '{args.name}'", log_type='error')
            return
        del context.cookies[args.name]
        log("Removed cookie:", log_type='cookie')
        log(f"   '{args.name}'")

    def _clear(self, _args: argparse.Namespace, context: Context):
        """
        This function clears the console cookies.
        """
        context.cookies = {}
        log("Stored cookies cleared", log_type='cookie')

###   end of file   ###
