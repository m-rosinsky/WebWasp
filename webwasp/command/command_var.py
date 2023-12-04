"""
file: src/command_var.py

This file contains the var command class.
"""

import argparse

from webwasp.logger import log
from webwasp.context import Context
from webwasp.node import CommandNode
from webwasp.command.command_interface import CommandInterface

class CommandVar(CommandInterface):
    """
    This class handles the var command, which stores text
    variables in the console context.
    """
    def __init__(self, name):
        super().__init__(name)

        # Create argument parser.
        self.parser = argparse.ArgumentParser(
            prog=self.name,
            description='Set local variables for the console',
            epilog="""
            To use variables in commands, preface the variable name with a '$' sign.
            Run command with no arguments to list all variables
            """,
            add_help=False
        )
        super().add_help(self.parser)

        # Create the subparser object.
        self.subparser = self.parser.add_subparsers()

        # Create the var add command subparser.
        self.parser_add = self.subparser.add_parser(
            'add',
            description='Add a variable',
            help='Add a variable',
            add_help=False,
        )
        self.parser_add.set_defaults(func=self._add)
        super().add_help(self.parser_add)
        self.parser_add.add_argument(
            'name',
            type=str,
            help='The name of the new variable',
        )
        self.parser_add.add_argument(
            'value',
            type=str,
            help='The value of the new variable',
        )

        # Create the var remove command subparser.
        self.parser_remove = self.subparser.add_parser(
            'remove',
            description='Remove a variable',
            help='Remove a variable',
            add_help=False,
        )
        self.parser_remove.set_defaults(func=self._remove)
        super().add_help(self.parser_remove)
        self.parser_remove.add_argument(
            'name',
            type=str,
            help='The name of the variable to remove',
        )

        # Create the var clear command subparser.
        self.parser_clear = self.subparser.add_parser(
            'clear',
            description='Remove all variables',
            help='Remove all variables',
            add_help=False,
        )
        self.parser_clear.set_defaults(func=self._clear)
        super().add_help(self.parser_clear)

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
        This function lists all variables currently stored.
        """
        log("Current stored variables:", log_type='info')
        for name, value in context.vars.items():
            log(f"   ${name} -> '{value}'")

    def _add(self, args: argparse.Namespace, context: Context):
        """
        This function adds a new variable.
        """
        if ':' in args.name:
            log(
                "Variable names cannot contain the ':' character",
                log_type='error',
            )
            return

        context.vars[args.name] = args.value
        log("Added variable:", log_type='info')
        log(f"   ${args.name} -> '{args.value}'")

    def _remove(self, args: argparse.Namespace, context: Context):
        """
        This function removes a parameter.
        """
        if args.name not in context.vars:
            log(f"Variable '{args.name}' does not exist", log_type='error')
            return
        
        del context.vars[args.name]
        log("Removed variable:", log_type='info')
        log(f"   ${args.name}")

    def _clear(self, args: argparse.Namespace, context: Context):
        """
        This function clears the context parameters.
        """
        context.vars = {}
        log("All variables cleared", log_type='info')

###   end of file   ###
