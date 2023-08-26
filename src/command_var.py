"""
file: src/command_var.py

This file contains the var command class.
"""

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

        # Add variable entry to console's var property.
        name = parse[1]
        val = parse[2]
        if console:
            console.vars[name] = val
            print(f"${name} -> {val}")

        # Export if flag is set.
        if export_flag:
            ### TODO: Exporting
            print("Exporting...")

        return True

###   end of file   ###
