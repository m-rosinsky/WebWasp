"""
file: src/command_headers.py

This file contains the headers command class.
"""

import argparse

from webwasp.logger import log
from webwasp.context import Context
from webwasp.node import CommandNode
from webwasp.command.command_interface import CommandInterface

# This holds header info fields.
INFO_FIELDS = {
    'accept': 'Media types that are acceptable for the response',
    'accept-language': 'Preferred language for the response',
    'accept-encoding': 'Types of client-supported encoding schemes',
    'cache-control': 'Directives for caching mechanisms',
    'connection': 'Should network connection stay open after transaction?',
    'if-modified-since': 'Conditional GET requests based on modif. time of resource',
    'host': 'Domain name of the server (for virtual hosting)',
    'referer': 'URL of the previous webpage, from which the request was initiated',
    'user-agent': 'Client application making the request',
}

class CommandHeaders(CommandInterface):
    """
    This class handles the headers command, which is used
    to set and unset different HTTP 1.1 header values.
    """
    def __init__(self, name):
        super().__init__(name)

        # Create argument parser and help.
        self.parser = argparse.ArgumentParser(
            prog=self.name,
            description='Modify the HTTP header fields for requests',
            add_help=False
        )
        super().add_help(self.parser)

        # Create the subparser object.
        self.subparser = self.parser.add_subparsers()

        # Create the headers add command subparser.
        self.parser_add = self.subparser.add_parser(
            'add',
            description='Add a header field',
            help='Add a header field',
            add_help=False
        )
        super().add_help(self.parser_add)
        self.parser_add.set_defaults(func=self._add)
        self.parser_add.add_argument(
            'name',
            type=str,
            help='The name of the header field',
        )
        self.parser_add.add_argument(
            'value',
            type=str,
            help='The header field value',
        )

        # Create the headers remove command subparser.
        self.parser_remove = self.subparser.add_parser(
            'remove',
            description='Remove a header field',
            help='Remove a header field',
            add_help=False,
        )
        super().add_help(self.parser_remove)
        self.parser_remove.set_defaults(func=self._remove)
        self.parser_remove.add_argument(
            'name',
            type=str,
            help='The header field to remove',
        )

        # Create the headers clear command subparser.
        self.parser_clear = self.subparser.add_parser(
            'clear',
            description='Remove all header fields',
            help='Remove all header fields',
            add_help=False,
        )
        super().add_help(self.parser_clear)
        self.parser_clear.set_defaults(func=self._clear)

        # Create the headers info command subparser.
        self.parser_info = self.subparser.add_parser(
            'info',
            description='Get info on common header field names',
            help='Get info on common header field names',
            add_help=False,
        )
        super().add_help(self.parser_info)
        self.parser_info.set_defaults(func=self._info)

    def create_cmd_tree(self) -> CommandNode:
        t = super().create_cmd_tree()

        nodes = []
        for field in INFO_FIELDS.keys():
            node = CommandNode(field)
            nodes.append(node)

        for child in t.children:
            if child.name in ['add', 'remove']:
                child.children = nodes

        return t

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
        This function lists all headers currently stored.
        """
        log("Current header fields:", log_type='info')
        for name, value in context.headers.items():
            log(f"   '{name}' : '{value}'")

    def _add(self, args: argparse.Namespace, context: Context):
        """
        This function adds a header field.
        """
        context.headers[args.name] = args.value
        log("Added header field:", log_type='info')
        log(f"   '{args.name}' : '{args.value}'")

    def _remove(self, args: argparse.Namespace, context: Context):
        """
        This function removes a header field.
        """
        if args.name not in context.headers:
            log(f"Unknown header field: '{args.name}'", log_type='error')
            return
        del context.headers[args.name]
        log("Removed header field", log_type='info')
        log(f"   '{args.name}'")

    def _clear(self, args: argparse.Namespace, context: Context):
        """
        This function unsets all header fields.
        """
        context.headers = {}
        log("Cleared all header fields", log_type='info')

    def _info(self, args: argparse.Namespace, context: Context):
        """
        This function gives some basic info about header fields.
        """
        longest_field_len = 0
        for name in INFO_FIELDS.keys():
            l = len(name)
            if l > longest_field_len:
                longest_field_len = l

        log("Common HTTP header fields:", log_type='info')
        for field, desc in INFO_FIELDS.items():
            num_spaces = longest_field_len - len(field) + 1
            log(f"   '\033[36m{field}\033[0m':{' '*num_spaces}{desc}")

###   end of file   ###
