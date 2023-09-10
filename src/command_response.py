"""
file: src/command_response.py

This file contains the response command class.
"""

import argparse

from src.command_interface import CommandInterface

class CommandResponse(CommandInterface):
    """
    This class handles the response command, which is used
    to interact with the most recent response stored in the console.
    """
    def __init__(self, name):
        super().__init__(name)

        # Create argument parser and help.
        self.parser = argparse.ArgumentParser(
            prog=self.name,
            description="Interact with the most recent response",
            add_help=False
        )
        super().add_help(self.parser)

        # Create the subparser object.
        self.subparser = self.parser.add_subparsers()

        # Create the response show command subparser.
        self.parser_show = self.subparser.add_parser(
            "show",
            description="Show the most recent response",
            help="Show the most recent response",
            add_help=False
        )
        self.parser_show.set_defaults(func=self._show)
        self.parser_show.add_argument(
            "-h",
            "--help",
            action="help",
            default=argparse.SUPPRESS,
            help="show this help message"
        )
        self.parser_show.add_argument(
            "-t",
            action="store_true",
            help="show the text of the response"
        )

        # Create the response report command subparser.
        self.parser_report = self.subparser.add_parser(
            "report",
            help="Generate a report of the last response"
        )
        self.parser_report.set_defaults(func=self._report)

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

        # If no subcommand was specified, show help.
        if not hasattr(args, "func"):
            self.parser.print_help()
            return True

        if not console.has_response:
            print("[🐝] No response captured")
            return True

        args.func(args, console)

        return True

    def _show(self, args, console):
        if args.t:
            self._show_text(console)
        else:
            self._show_summary(console)

    def _show_summary(self, console):
        console.response.print_summary()
        print("\nRe-run 'response show' with '-t' option to show response text")

    def _show_text(self, console):
        print(console.response.req.text)

    def _report(self, args, console):
        print("report")

###   end of file   ###
