"""
file: src/command/command.py

This file contains the dispatch method for commands.

It is responsible for parsing and dispatching a command to
its respective module for handling.
"""

from src.command_get import CommandGet
from src.command_var import CommandVar
from src.command_clear import CommandClear
from src.command_params import CommandParams
from src.command_timeout import CommandTimeout
from src.command_response import CommandResponse
from src.command_interface import CommandInterface

class CommandHelp(CommandInterface):
    """
    This is the class to handle help commands.

    It is consolidated within the dispatch so it can reference
    the other command class instances without circular dependencies.
    """
    def __init__(self, name):
        super().__init__(name)

    def run(self, parse, console=None):
        super().run(parse)

        parse_len = len(parse)
        # Check usage.
        if parse_len != 1:
            print("[🛑] Error: Invalid arguments")
            print("Run any command with '-h' option for more specific help")
            return True

        # Get generalized help.
        for _, obj in command_dict.items():
            if obj.parser is not None:
                print(f"{obj.name}", end="")

                # Determine number of tabs so all indents are aligned.
                num_tabs = 1 if len(obj.name) >= 8 else 2
                for _ in range(num_tabs):
                    print("\t", end="")

                print(f"{obj.parser.description}")

        print("\nRun any command with '-h' option for more specific help")
        return True

# This defines the global mapping of command names to their respective classes.
command_var = CommandVar("var")
command_get = CommandGet("get")
command_help = CommandHelp("help")
command_clear = CommandClear("clear")
command_params = CommandParams("params")
command_timeout = CommandTimeout("timeout")
command_response = CommandResponse("response")

command_dict = {
    "help"      : command_help,
    "clear"     : command_clear,
    "var"       : command_var,
    "get"       : command_get,
    "response"  : command_response,
    "timeout"   : command_timeout,
    "params"    : command_params,
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
