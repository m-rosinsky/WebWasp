"""
file: src/command_response.py

This file contains the response command class.
"""

import argparse
from bs4 import BeautifulSoup

from src.logger import log
from src.command.command_interface import CommandInterface

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
            description='Interact with the most recent response',
            add_help=False
        )
        super().add_help(self.parser)

        # Create the subparser object.
        self.subparser = self.parser.add_subparsers()

        # Create the response show command subparser.
        self.parser_show = self.subparser.add_parser(
            'show',
            description='Show the most recent response',
            help='Show the most recent response',
            add_help=False
        )
        self.parser_show.set_defaults(func=self._show)
        super().add_help(self.parser_show)
        self.parser_show.add_argument(
            '-t',
            '--text',
            action='store_true',
            help='show the text of the response'
        )
        self.parser_show.add_argument(
            '-c',
            '--cookies',
            action='store_true',
            help='show the cookies of the response'
        )

        # Create the response report command subparser.
        self.parser_report = self.subparser.add_parser(
            'report',
            help='Generate a report of the last response',
            add_help=False,
        )
        self.parser_report.set_defaults(func=self._report)
        super().add_help(self.parser_report)

        # Create the response beautify command subparser.
        self.parser_beautify = self.subparser.add_parser(
            'beautify',
            help='Clean up response text with HTML encoding',
            add_help=False,
        )
        self.parser_beautify.set_defaults(func=self._beautify)
        super().add_help(self.parser_beautify)

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

        # If no subcommand was specified, show help.
        if not hasattr(args, 'func'):
            self.parser.print_help()
            return True

        if not console.has_response:
            log("No response captured", log_type='warning')
            return True

        args.func(args, console)

        return True

    def _show(self, args, console):
        if args.text:
            print(console.response.req_text)
        elif args.cookies:
            console.response.print_cookies()
        else:
            self._show_summary(console)

    def _show_summary(self, console):
        console.response.print_summary()
        log("\nRe-run 'response show' with '-t' option to show response text")

    def _report(self, args, console):
        log("report")

    def _beautify(self, args, console):
        """
        This function decodes HTML entities.
        """
        entity_table = {
            '&nbsp;' : ' ',
            '&lt;' : '<',
            '&gt;' : '>',
            '&amp;' : '&',
            '&quot;' : '\"',
            '&apos;' : '\'',
            '&cent;' : '¢',
            '&pound;' : '£',
            '&yen;' : '¥',
            '&euro;' : '€',
            '&copy;' : '©',
            '&reg;' : '®',
        }

        text = str(console.response.req_text)

        log("Beautifying response text...", log_type='info')

        num_repls = 0
        for entity, repl in entity_table.items():
            num_repls += len(text.split(entity)) - 1
            text = text.replace(entity, repl)

        # Run bs4's prettify.
        text = BeautifulSoup(text, 'html.parser').prettify()

        console.response.req_text = text

        log(f"   Done! Made \033[36m{num_repls}\033[0m replacements.")

###   end of file   ###
