"""
file: src/command/command.py

This file contains the dispatch method for commands.

It is responsible for parsing and dispatching a command to
its respective module for handling.
"""

from src.command_help import Command_Help

# This defines the global mapping of command names to their respective classes.
command_help = Command_Help("help")

command_dict = {
    "help" : command_help,
}

def dispatch(cmd):
    """
    This function parses and dispatches a given command.

    Args:
    cmd - The command to handle.

    Returns:
    False if console should exit after command, True otherwise.
    """
    # Parse the command.
    parse = cmd.split()

    # Test for blank command.
    if len(parse) == 0:
        return True

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
    return command_class.run(parse)

###   end of file   ###
