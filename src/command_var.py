"""
file: src/command_var.py

This file contains the var command class.
"""

import os
import argparse

from src.command_interface import CommandInterface

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
            description="Set local variables for the console. Run command with no arguments to list all variables",
            epilog="To use variables in commands, preface the variable name with a '$' sign",
            add_help=False
        )

        # Add argparse args.
        self.parser.add_argument(
            'name',
            type=str,
            help='The name of the new variable'
        )
        self.parser.add_argument(
            'value',
            type=str,
            help='The value of the new variable'
        )
        self.parser.add_argument(
            '-e',
            action='store_true',
            help='Export the variable so it is saved between sessions',
        )

    def get_help(self):
        super().get_help()

    def get_usage(self):
        super().get_usage()
        print("var [name value [-e]]\n")

        print("Arguments:")
        print("  name  - The variable name")
        print("  value - The value for the variable")
        print("  [-e]  - Export the variable so it is saved b/w sessions")

    def run(self, parse, console):
        super().run(parse)

        # If no arguments, list out all variables.
        parse_len = len(parse)
        if parse_len == 1:
            for name, val in console.vars.items():
                print(f"${name} -> '{val}'")
            return True

        # Slice the command name off the parse so we only
        # parse the arguments.
        parse_trunc = parse[1:]

        try:
            args = self.parser.parse_args(parse_trunc)
        except argparse.ArgumentError:
            self.get_help()
            return True
        except SystemExit:
            # Don't let argparse exit the program.
            return True

        # Extract arguments.
        name = args.name
        val = args.value
        export_flag = args.e

        # Variable names are not allowed to include the ":" character,
        # since it is used in formatting of export files.
        if ":" in name:
            print("[🛑] Error: var names cannot contain the ':' character")
            return True

        # Add variable entry to console's var property.
        console.vars[name] = val
        print(f"${name} -> {val}")

        # Export if flag is set.
        if export_flag:
            exp_status = self._export_var(name, val, console)
            if exp_status:
                print("Exported successfully")
            else:
                print("[🛑] Error: Failed to export variable")

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
                with open(console.export_file, "w", encoding="utf-8") as exp_f:
                    pass
                os.chmod(console.export_file, 0o666) # rw-rw-rw

            # Construct entry string.
            entry_string = f"{name}:{val}"

            # Read existing data and update or add the entry.
            updated_lines = []
            entry_found = False
            with open(console.export_file, "r", encoding="utf-8") as exp_f:
                for line in exp_f:
                    line_name, _ = line.strip().split(":", 1)
                    if line_name == name:
                        updated_lines.append(entry_string)
                        entry_found = True
                    else:
                        updated_lines.append(line.strip())

            if not entry_found:
                updated_lines.append(entry_string)

            # Write updated data back to the file.
            with open(console.export_file, "w", encoding="utf-8") as exp_f:
                for line in updated_lines:
                    exp_f.write(line + "\n")

            return True
        except OSError as open_err:
            print(f"{open_err}")
            return False

###   end of file   ###
