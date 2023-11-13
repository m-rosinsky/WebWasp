"""
file: src/command_response.py

This file contains the response command class.
"""

import argparse
import re
from bs4 import BeautifulSoup

from src.logger import log
from src.response import html_highlight
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
            help='show the text of the response',
        )
        self.parser_show.add_argument(
            '-c',
            '--cookies',
            action='store_true',
            help='show the cookies of the response',
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

        # Create the response find command subparser.
        self.parser_find = self.subparser.add_parser(
            'find',
            help='Find specific things within the response',
            add_help=False
        )
        self.parser_find.set_defaults(func=self._find)
        super().add_help(self.parser_find)
        self.parser_find.add_argument(
            '--tag',
            metavar='tag',
            type=str,
            help='Find all items with a given HTML tag in response',
        )
        self.parser_find.add_argument(
            '-t',
            '--text',
            action='store_true',
            help='Find all text in response',
        )
        self.parser_find.add_argument(
            '-l',
            '--links',
            action='store_true',
            help='Find all links in response',
        )
        self.parser_find.add_argument(
            '--title',
            action='store_true',
            help='Find the <title> of the HTML response',
        )
        self.parser_find.add_argument(
            '-c',
            '--class',
            dest='find_class', # .class is reserved in python.
            metavar='name',
            type=str,
            help='Find all HTML tags with a given class name',
        )
        self.parser_find.add_argument(
            '-i',
            '--id',
            metavar='id',
            type=str,
            help='Find all HTML tags with a given id',
        )
        self.parser_find.add_argument(
            '--strip',
            action='store_true',
            help='Don\'t show HTML tags in find results',
        )

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
            console.response.print_text()
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

        text = str(console.response.req.text)

        log("Beautifying response text...", log_type='info')

        # Run bs4's prettify.
        text = BeautifulSoup(text, 'html.parser').prettify()

        num_repls = 0
        for entity, repl in entity_table.items():
            num_repls += len(text.split(entity)) - 1
            text = text.replace(entity, repl)

        console.response.req_text = text

        log(f"   Ran \033[36mprettify\033[0m.")
        log(f"   Made \033[36m{num_repls}\033[0m entity decodes.")

    def _find(self, args, console):
        """
        This function finds and prints specific items within
        the stored response. This does not alter the stored
        response.
        """
        # Generate soup.
        # text = BeautifulSoup(console.response.req_text, 'html.parser').prettify()
        soup = BeautifulSoup(console.response.req_text, 'html.parser')

        has_query = False
        matches = []

        # Paragraphs.
        if args.tag:
            has_query = True
            for t in soup.find_all(args.tag):
                if args.strip:
                    t = t.string
                matches.append(t)

        # Text.
        if args.text:
            has_query = True
            soup_text = soup.get_text()
            for t in soup_text.split("\n"):
                t = t.strip()
                if len(t) > 0:
                    matches.append(t)

        # Links.
        if args.links:
            has_query = True
            for link in soup.find_all('a'):
                matches.append(link.get('href'))

        # Title.
        if args.title:
            has_query = True
            t = soup.title
            if args.strip:
                t = t.string
            matches.append(t)

        # Classes.
        if args.find_class:
            has_query = True
            for c in soup.find_all(class_=args.find_class):
                if args.strip:
                    c = c.string
                matches.append(c)

        # Id.
        if args.id:
            has_query = True
            for i in soup.find_all(id=args.id):
                if args.strip:
                    i = i.string
                matches.append(i)

        # Check if no query was specified.
        if not has_query:
            log('No query given to find command', log_type='warning')
            return

        # Print findings.
        log("Find results:", log_type='info')

        for m in matches:
            line = html_highlight(str(m), style='lovelace').strip()
            log(line)

###   end of file   ###
