"""
file: src/command_params.py

This file contains the params command class.
"""

import argparse

from src.logger import log
from src.command.command_interface import CommandInterface

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
        This function lists all parameters currently stored.
        """
        log("Current stored parameters:", log_type='info')
        for name, value in console.params.items():
            log(f"   '{name}' : '{value}'")

    def _add(self, args, console):
        """
        This function adds a new parameter.
        """
        console.params[args.name] = args.value
        log("Added param:", log_type='info')
        log(f"   '{args.name}' : '{args.value}'")

    def _remove(self, args, console):
        """
        This function removes a parameter.
        """
        if args.name not in console.params:
            log(f"Unknown parameter: '{args.name}'", log_type='error')
            return
        del console.params[args.name]
        log("Removed param", log_type='info')
        log(f"   '{args.name}'")

    def _clear(self, args, console):
        """
        This function clears the console parameters.
        """
        console.params = {}
        log("Stored parameters cleared", log_type='info')

###   end of file   ###
