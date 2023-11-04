"""
file: src/command_var.py

This file contains the var command class.
"""

import os
import argparse

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

        # TODO: Write console variables to file for persistence.

        return True

    def _export_var(self, name, val, console):
        """
        This function writes a variable name/value pair to the export
        file.

        Args:
        name - The variable name.
        val  - The variable value.
        console - The console context to pull the export file name.

        Returns:
        True on success, False on failure.
        """
        try:
            # Create file if doesn't exist.
            if not os.path.exists(console.export_file):
                with open(console.export_file, 'w', encoding='utf-8') as exp_f:
                    pass
                os.chmod(console.export_file, 0o666) # rw-rw-rw

            # Construct entry string.
            entry_string = f"{name}:{val}"

            # Read existing data and update or add the entry.
            updated_lines = []
            entry_found = False
            with open(console.export_file, 'r', encoding='utf-8') as exp_f:
                for line in exp_f:
                    line_name, _ = line.strip().split(':', 1)
                    if line_name == name:
                        updated_lines.append(entry_string)
                        entry_found = True
                    else:
                        updated_lines.append(line.strip())

            if not entry_found:
                updated_lines.append(entry_string)

            # Write updated data back to the file.
            with open(console.export_file, 'w', encoding='utf-8') as exp_f:
                for line in updated_lines:
                    exp_f.write(line + '\n')

            return True
        except OSError as open_err:
            print(f"{open_err}")
            return False

    def _list(self, console):
        """
        This function lists all variables currently stored.
        """
        print("Current stored variables:")
        for name, value in console.vars.items():
            print(f"   ${name} -> '{value}'")

    def _add(self, args, console):
        """
        This function adds a new variable.
        """
        if ':' in args.name:
            print("[🛑] Error: var names cannot contain the ':' character")
            return

        console.vars[args.name] = args.value
        print("[🟢] Added variable:")
        print(f"   ${args.name} -> '{args.value}")

    def _remove(self, args, console):
        """
        This function removes a parameter.
        """
        if args.name not in console.vars:
            print(f"[⚠] Variable '{args.name}' does not exist")
            return
        del console.vars[args.name]
        print("[🟢] Removed variable:")
        print(f"   ${args.name}")

    def _clear(self, args, console):
        """
        This function clears the console parameters.
        """
        console.vars = {}
        print("[🟢] All variables cleared")

###   end of file   ###
