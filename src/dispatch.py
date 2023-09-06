"""
file: src/command/command.py

This file contains the dispatch method for commands.

It is responsible for parsing and dispatching a command to
its respective module for handling.
"""

from src.command_interface import CommandInterface
from src.command_response import CommandResponse
from src.command_timeout import CommandTimeout
from src.command_clear import CommandClear
from src.command_var import CommandVar
from src.command_get import CommandGet

class CommandHelp(CommandInterface):
    """
    This is the class to handle help commands.

    It is consolidated within the dispatch so it can reference
    the other command class instances without circular dependencies.
    """
    def __init__(self, name):
        super().__init__(name)

    def get_help(self):
        super().get_help()
        print("Description:")
        print("  Get general help, or help for a specified command\n")
        self.get_usage()

    def get_usage(self):
        super().get_usage()
        print("help [cmd]\n")

        print("Arguments:")
        print("  [cmd] - Optional command to get help entry for")

    def run(self, parse, console=None):
        super().run(parse)

        parse_len = len(parse)
        # Check usage.
        if parse_len > 2:
            print("[🛑] Error: Extra arguments\n")
            self.get_usage()
            return True

        # If command is specified, ensure it exists.
        if parse_len == 2:
            help_entry = command_dict.get(parse[1])
            if not help_entry:
                print(f"No help entry for command: '{parse[1]}'")
            else:
                help_entry.get_help()
            return True

        # Get generalized help.
        print("Getting general help...")
        return True

# This defines the global mapping of command names to their respective classes.
command_help = CommandHelp("help")
command_clear = CommandClear("clear")
command_var = CommandVar("var")
command_get = CommandGet("get")
command_response = CommandResponse("response")
command_timeout = CommandTimeout("timeout")

command_dict = {
    "help"      : command_help,
    "h"         : command_help,
    "clear"     : command_clear,
    "cls"       : command_clear,
    "var"       : command_var,
    "get"       : command_get,
    "resp"      : command_response,
    "response"  : command_response,
    "timeout"   : command_timeout,
}

def dispatch(cmd, vars, console):
    """
    This function parses and dispatches a given command.

    Args:
    cmd - The command to handle.
    vars - The list of vars stored for the console.

    Returns:
    False if console should exit after command, True otherwise.
    """
    # Parse the command.
    parse = cmd.split()

    # Test for blank command.
    if len(parse) == 0:
        return True

    # Resolve variable names.
    for i in range(len(parse)):
        token = parse[i]
        if token[0] == "$":
            # Look up variable in console.
            name = token[1:]
            val = console.vars.get(name)
            if not val:
                print(f"[🛑] Error: Unknown variable: {name}")
                return True
            
            # Perform replacement.
            parse[i] = val

    # Check for quit. This can be given its own command class definition
    # if more complexity needs to be added in the future.
    if parse[0] == "quit" or parse[0] == "exit" or parse[0] == "q":
        return False

    # Check if command exists.
    if parse[0] not in command_dict:
        print(f"Unknown command: '{parse[0]}'")
        return True

    # Run command.
    command_class = command_dict.get(parse[0])
    return command_class.run(parse, console)

###   end of file   ###
