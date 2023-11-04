"""
file: src/command_cookies.py

This file contains the cookies command class.
"""

import argparse

from src.command.command_interface import CommandInterface

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
            description="Modify the cookies for requests",
            add_help=False
        )
        super().add_help(self.parser)

        # Create the subparser object.
        self.subparser = self.parser.add_subparsers()

        # Create the cookies add command subparser.
        self.parser_add = self.subparser.add_parser(
            "add",
            description="Add a cookie",
            help="Add a cookie",
            add_help=False
        )
        self.parser_add.set_defaults(func=self._add)
        self.parser_add.add_argument(
            "name",
            type=str,
            help="The name of the new cookie"
        )
        self.parser_add.add_argument(
            "value",
            type=str,
            help="The value of the new cookie"
        )

        # Create the params remove command subparser.
        self.parser_remove = self.subparser.add_parser(
            "remove",
            description="Remove a cookie",
            help="Remove a cookie",
            add_help=False
        )
        self.parser_remove.set_defaults(func=self._remove)
        self.parser_remove.add_argument(
            "name",
            type=str,
            help="The name of the cookie to remove"
        )

        # Create the params clear command subparser.
        self.parser_clear = self.subparser.add_parser(
            "clear",
            description="Remove all cookies",
            help="Remove all cookies",
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
        if not hasattr(args, "func"):
            self._list(console)
            return True

        args.func(args, console)

        # TODO: Write console cookies to file for persistence.

        return True

    def _list(self, console):
        """
        This function lists all cookies currently stored.
        """
        print("Current stored cookies:")
        for name, value in console.cookies.items():
            print(f"   '{name}' : '{value}'")

    def _add(self, args, console):
        """
        This function adds a new cookie.
        """
        console.cookies[args.name] = args.value
        print("Added cookie:\n   ", end="")
        print(f"'{args.name}' : '{args.value}'")

    def _remove(self, args, console):
        """
        This function removes a cookie.
        """
        if args.name not in console.cookies:
            print(f"Unknown cookie: '{args.name}'")
            return
        del console.cookies[args.name]
        print("Removed cookie\n   ", end="")
        print(f"'{args.name}'")

    def _clear(self, args, console):
        """
        This function clears the console cookies.
        """
        console.cookies = {}
        print("Stored cookies cleared")

###   end of file   ###
