"""
file: src/command_params.py

This file contains the params command class.
"""

import argparse

from webwasp.logger import log
from webwasp.context import Context
from webwasp.node import CommandNode
from webwasp.command.command_interface import CommandInterface

class CommandParams(CommandInterface):
    """
    This class handles the params command, which is used
    to assign parameters passed into urls for requests.
    """
    def __init__(self, name):
        super().__init__(name)

        # Create argument parser and help.
        self.parser = argparse.ArgumentParser(
            prog=self.name,
            description='Modify the url parameters for requests',
            add_help=False
        )
        super().add_help(self.parser)

        # Create the subparser object.
        self.subparser = self.parser.add_subparsers()

        # Create the params add command subparser.
        self.parser_add = self.subparser.add_parser(
            'add',
            description='Add a parameter',
            help='Add a parameter',
            add_help=False
        )
        self.parser_add.set_defaults(func=self._add)
        self.parser_add.add_argument(
            'name',
            type=str,
            help='The name of the new param'
        )
        self.parser_add.add_argument(
            'value',
            type=str,
            help='The value of the new param'
        )

        # Create the params remove command subparser.
        self.parser_remove = self.subparser.add_parser(
            'remove',
            description='Remove a parameter',
            help='Remove a parameter',
            add_help=False
        )
        self.parser_remove.set_defaults(func=self._remove)
        self.parser_remove.add_argument(
            'name',
            type=str,
            help='The name of the param to remove'
        )

        # Create the params clear command subparser.
        self.parser_clear = self.subparser.add_parser(
            'clear',
            description='Remove all parameters',
            help='Remove all parameters',
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
        This function lists all parameters currently stored.
        """
        log("Current stored parameters:", log_type='info')
        for name, value in context.params.items():
            log(f"   '{name}' : '{value}'")

    def _add(self, args: argparse.Namespace, context: Context):
        """
        This function adds a new parameter.
        """
        context.params[args.name] = args.value
        log("Added param:", log_type='info')
        log(f"   '{args.name}' : '{args.value}'")

    def _remove(self, args: argparse.Namespace, context: Context):
        """
        This function removes a parameter.
        """
        if args.name not in context.params:
            log(f"Unknown parameter: '{args.name}'", log_type='error')
            return
        del context.params[args.name]
        log("Removed param", log_type='info')
        log(f"   '{args.name}'")

    def _clear(self, args: argparse.Namespace, context: Context):
        """
        This function clears the context parameters.
        """
        context.params = {}
        log("Stored parameters cleared", log_type='info')

###   end of file   ###
