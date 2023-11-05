"""
file: src/command_var.py

This file contains the var command class.
"""

import argparse

from src.logger import log
from src.command.command_interface import CommandInterface

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

        # If no subcommand was specified, show list.
        if not hasattr(args, 'func'):
            self._list(console)
            return True

        args.func(args, console)
        console.update_data()

        return True

    def _list(self, console):
        """
        This function lists all variables currently stored.
        """
        log("Current stored variables:", log_type='info')
        for name, value in console.vars.items():
            log(f"   ${name} -> '{value}'")

    def _add(self, args, console):
        """
        This function adds a new variable.
        """
        if ':' in args.name:
            log(
                "Variable names cannot contain the ':' character",
                log_type='error',
            )
            return

        console.vars[args.name] = args.value
        log("Added variable:", log_type='info')
        log(f"   ${args.name} -> '{args.value}'")

    def _remove(self, args, console):
        """
        This function removes a parameter.
        """
        if args.name not in console.vars:
            log(f"Variable '{args.name}' does not exist", log_type='error')
            return
        
        del console.vars[args.name]
        log("Removed variable:", log_type='info')
        log(f"   ${args.name}")

    def _clear(self, args, console):
        """
        This function clears the console parameters.
        """
        console.vars = {}
        log("All variables cleared", log_type='info')

###   end of file   ###
