"""
file: webwasp/command/command_auth.py

This file contains the auth command class.
"""

import argparse

from webwasp.logger import log
from webwasp.context import Context
from webwasp.node import CommandNode
from webwasp.command.command_interface import CommandInterface

class CommandAuth(CommandInterface):
    """
    This class handles the auth command, which is used to set
    the 401 auth fields for requests.
    """
    def __init__(self, name):
        super().__init__(name)

        # Create argument parser and help.
        self.parser = argparse.ArgumentParser(
            prog=self.name,
            description='Modify the HTTP Authorization fields for requests',
            add_help=False,
        )
        super().add_help(self.parser)

        # Create the subparser object.
        self.subparser = self.parser.add_subparsers()

        # Create the auth user command subparser.
        self.parser_user = self.subparser.add_parser(
            'user',
            description='Set the authorization username',
            help='Set the authorization username',
            add_help=False,
        )
        super().add_help(self.parser_user)
        self.parser_user.set_defaults(func=self._user)
        self.parser_user.add_argument(
            'value',
            type=str,
            help='The username to authorize',
        )

        # Create the auth pass command subparser.
        self.parser_pass = self.subparser.add_parser(
            'pass',
            description='Set the authorization password',
            help='Set the authorization password',
            add_help=False,
        )
        super().add_help(self.parser_pass)
        self.parser_pass.set_defaults(func=self._pass)
        self.parser_pass.add_argument(
            'value',
            type=str,
            help='The password to authorize',
        )

        # Create the auth clear command subparser.
        self.parser_clear = self.subparser.add_parser(
            'clear',
            description='Unset auth fields',
            help='Unset auth fields',
            add_help=False,
        )
        super().add_help(self.parser_clear)
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
        This function lists the auth fields.
        """
        log("Current auth fields:", log_type='info')
        log(f"   'user': '{context.auth.get('user', '')}'")
        log(f"   'pass': '{context.auth.get('pass', '')}'")

    def _user(self, args: argparse.Namespace, context: Context):
        """
        This function sets the user field.
        """
        context.auth['user'] = args.value
        log("Set 'user' auth field:", log_type='info')
        log(f"   '{args.value}'")

    def _pass(self, args: argparse.Namespace, context: Context):
        """
        This function sets the pass field.
        """
        context.auth['pass'] = args.value
        log("Set 'pass' auth field:", log_type='info')
        log(f"   '{args.value}'")

    def _clear(self, args: argparse.Namespace, context: Context):
        """
        This function unsets all auth fields.
        """
        context.auth['user'] = None
        context.auth['pass'] = None
        log("Cleared auth fields", log_type='info')
        