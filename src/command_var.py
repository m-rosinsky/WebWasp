"""
file: src/command_var.py

This file contains the var command class.
"""

import os

from src.command_interface import CommandInterface

class CommandVar(CommandInterface):
    """
    This class handles the var command, which stores text
    variables in the console context.
    """
    def __init__(self, name):
        super().__init__(name)

    def get_help(self):
        super().get_help()
        print("Description:")
        print("  Set local variables for the console.")
        print("  Run command with no arguments to list all variables")
        print("")
        print("  To use variables in commands, simply preface the")
        print("  variable name with a '$' sign.")
        print("")
        self.get_usage()

    def get_usage(self):
        super().get_usage()
        print("var [name value [-e]]\n")

        print("Arguments:")
        print("  name  - The variable name")
        print("  value - The value for the variable")
        print("  [-e]  - Export the variable so it is saved b/w sessions")

    def run(self, parse, console=None):
        super().run(parse)

        # Ensure console exists.
        if not console:
            print("[🛑] Error: Missing console context in var call")
            return False

        # If no arguments, list out all variables.
        parse_len = len(parse)
        if parse_len == 1:
            for name, val in console.vars.items():
                print(f"${name} -> '{val}'")
            return True

        # Check usage.
        if parse_len < 3 or parse_len > 4:
            print("[🛑] Error: Invalid number of arguments\n")
            self.get_usage()
            return True

        # If fourth argument is specified, it must be "-e"
        export_flag = False
        if parse_len == 4:
            if parse[3] != "-e":
                print(f"[🛑] Error: Invalid argument: '{parse[3]}'")
                return True
            export_flag = True

        # Variable names are not allowed to include the ":" character,
        # since it is used in formatting of export files.
        name = parse[1]
        val = parse[2]
        if ":" in name:
            print("[🛑] Error: var names cannot contain the ':' character")
            return True

        # Add variable entry to console's var property.
        if console:
            console.vars[name] = val
            print(f"${name} -> {val}")

        # Export if flag is set.
        if export_flag:
            exp_status = self._export_var(name, val, console)
            if exp_status:
                print("Exported successfully")
            else:
                print("Failed to export variable")

        return True
    
    def _export_var(self, name, val, console):
        """
        This functions writes a variable name/value pair to the export
        file.

        Args:
        name - The variable name.
        val  - The variable value.
        console - The console context to pull the export file name.

        Returns:
        True on success, False on failure.
        """
        # Create file if doesn't exist.
        if not os.path.exists(console.export_file):
            with open(console.export_file, "w") as ef:
                pass

        # Open the file.
        raw_file_data = ""
        with open(console.export_file, "r", encoding="utf-8") as ef:
            # Read the file
            for line in ef:
                raw_file_data += line

        # Construct entry string.
        entry_string = f"{name}:{val}"

        # Find entry.
        entry_found = False
        file_lines = raw_file_data.split()
        for i in range(len(file_lines)):
            line_name = file_lines[i].split(":")[0]
            if line_name == name:
                file_lines[i] = entry_string
                entry_found = True
                break

        if not entry_found:
            file_lines.append(entry_string)

        # Write data.
        with open(console.export_file, "w", encoding="utf-8") as ef:
            for line in file_lines:
                ef.write(line + "\n")

        return True

###   end of file   ###
