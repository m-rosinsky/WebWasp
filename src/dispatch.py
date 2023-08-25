"""
file: src/command/command.py

This file contains the dispatch method for commands.

It is responsible for parsing and dispatching a command to
its respective module for handling.
"""

def parse_cmd(cmd):
    """
    This function parses a command and splits along whitespace.

    args:
    cmd - The command to parse.

    Returns:
    List of parsed command.
    """
    return cmd.split()

def dispatch(cmd):
    """
    This function parses and dispatches a command.

    Args:
    cmd - The command to handle

    Returns:
    False if console should exit. True otherwise.
    """
    # Parse the command.
    parse = parse_cmd(cmd)

    if len(cmd) == 0:
        return True

    # Quit command.
    if parse[0] == "quit" or parse[0] == "exit" or parse[0] == "q":
        return False

    print(parse)

    return True

###   end of file   ###
