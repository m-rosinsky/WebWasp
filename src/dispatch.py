"""
file: src/command/command.py

This file contains the dispatch method for commands.

It is responsible for parsing and dispatching a command to
its respective module for handling.
"""

import shlex

from src.logger import log
from src.command.command_get import CommandGet
from src.command.command_var import CommandVar
from src.command.command_clear import CommandClear
from src.command.command_params import CommandParams
from src.command.command_post import CommandPost
from src.command.command_cookies import CommandCookies
from src.command.command_headers import CommandHeaders
from src.command.command_timeout import CommandTimeout
from src.command.command_response import CommandResponse
from src.command.command_interface import CommandInterface

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
            log("Error: Invalid arguments", log_type='error')
            log("Run any command with '-h' option for more specific help")
            return True

        # Get generalized help.
        for _, obj in command_dict.items():
            if obj.parser is not None:
                log(f"{obj.name}", end="")

                # Determine number of tabs so all indents are aligned.
                num_tabs = 1 if len(obj.name) >= 8 else 2
                for _ in range(num_tabs):
                    log("\t", end="")

                log(f"{obj.parser.description}")

        log("\nRun any command with '-h' option for more specific help")
        return True

# This defines the global mapping of command names to their respective classes.
command_clear = CommandClear("clear")
command_cookies = CommandCookies("cookies")
command_get = CommandGet("get")
command_headers = CommandHeaders("headers")
command_help = CommandHelp("help")
command_params = CommandParams("params")
command_post = CommandPost("post")
command_response = CommandResponse("response")
command_timeout = CommandTimeout("timeout")
command_var = CommandVar("var")

command_dict = {
    "clear"     : command_clear,
    "cookies"   : command_cookies,
    "get"       : command_get,
    "headers"   : command_headers,
    "help"      : command_help,
    "params"    : command_params,
    "post"      : command_post,
    "response"  : command_response,
    "timeout"   : command_timeout,
    "var"       : command_var,
}

def _get_cmd_match(cmd):
    """
    Brief:
        This function attempts to match the entered command with
        the closest fit in the command dict.

        For example, if "timeout" is the only command in the dict that
        starts with the letter "t", then the user should be able to
        enter "t" and this function will resolve that.

    Arguments:
        cmd: str
            The command entered by the user

    Returns:
        String with the command on success, None on error.
    """
    matches = [command for command in command_dict if command.startswith(cmd)]

    # If the list contains a single entry, this is a success.
    if len(matches) == 1:
        return matches[0]

    # If the list comprehension returned multiple values, then the command
    # was ambiguous.
    if len(matches) > 1:
        log(f"Ambiguous command: '{cmd}'. Potential matches:", log_type='error')
        for match in matches:
            log(f"   {match}")
        return None
    
    # No matches were returned, so the command was invalid.
    log(f"Error: Unknown command '{cmd}'", log_type='error')

def dispatch(cmd, console):
    """
    This function parses and dispatches a given command.

    Args:
    cmd - The command to handle.

    Returns:
    False if console should exit after command, True otherwise.
    """
    # Parse the command.
    parse = shlex.split(cmd)

    # Test for blank command.
    if len(parse) == 0:
        return True

    # Resolve variable names.
    for i in range(len(parse)):
        token = parse[i]
        if token[0] == '$':
            # Look up variable in console.
            name = token[1:]
            val = console.vars.get(name)
            if not val:
                log(f"Error: Unknown variable: {name}", log_type='error')
                return True
            
            # Perform replacement.
            parse[i] = val

    # Check for quit. This can be given its own command class definition
    # if more complexity needs to be added in the future.
    if parse[0] == "quit" or parse[0] == "exit" or parse[0] == "q":
        return False

    # Get command best fit.
    matched_cmd = _get_cmd_match(parse[0])
    if matched_cmd is None:
        return True

    # Run command.
    command_class = command_dict.get(matched_cmd)
    return command_class.run(parse, console)

###   end of file   ###
