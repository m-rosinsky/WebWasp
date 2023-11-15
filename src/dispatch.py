"""
File:
    src/dispatch.py

Brief:
    This file acts as the main focal point of the program.

    This file contains a current context for tracking current session
    information, a console for prompting for commands, and a dispatch
    mechanism for dispatching a command to the appropriate handler.
"""

import os
import shlex

from src.console import Console
from src.context import Context
from src.logger import log
from src.node import CommandNode

from src.command.command_clear import CommandClear
from src.command.command_console import CommandConsole
from src.command.command_cookies import CommandCookies
from src.command.command_get import CommandGet
from src.command.command_headers import CommandHeaders
from src.command.command_params import CommandParams
from src.command.command_post import CommandPost
from src.command.command_response import CommandResponse
from src.command.command_timeout import CommandTimeout
from src.command.command_var import CommandVar

# The name for file to write command history to.
HISTORY_FILE = "~/.wwhistory"

# The name for the file to write session data to.
DATA_FILE = "~/.wwdata"

class Dispatcher:
    """
    Brief:
        This class functions as the dispatcher for dispatching commands
        to their appropriate handlers.

        It also contains a context for current session information.
    """
    def __init__(self):
        # The history and data files.
        self.history_file = os.path.expanduser(HISTORY_FILE)
        self.data_file = os.path.expanduser(DATA_FILE)

        # The current session context.
        self.context = Context(filename=self.data_file)

        # The command dictionary, consisting of all command classes and
        # the associated command names.
        self.command_dict = {
            'clear'     : CommandClear('clear'),
            'console'   : CommandConsole('console'),
            'cookies'   : CommandCookies('cookies'),
            'get'       : CommandGet('get'),
            'headers'   : CommandHeaders('headers'),
            'params'    : CommandParams('params'),
            'post'      : CommandPost('post'),
            'response'  : CommandResponse('response'),
            'timeout'   : CommandTimeout('timeout'),
            'var'       : CommandVar('var'),
        }

        # Build the command autocomp tree.
        self.cmd_tree = self._build_cmd_tree()

        # The console object, using the history file to track command history
        # and the command tree for autocompletions.
        self.console = Console(
            history_file=self.history_file,
            cmd_tree = self.cmd_tree,
        )

    def run(self):
        """
        Brief:
            This function serves as the main run loop of the program.

            It uses the console to prompt for a command, parses the command,
            the dispatches it to the appropriate handler.
        """
        # Run indefinitely.
        while True:
            # Prompt for a command.
            try:
                cmd = self.console.prompt()
            except KeyboardInterrupt:
                print("^C")
                break

            # Parse the command with shlex.
            try:
                cmd_parse = shlex.split(cmd)
            except ValueError:
                log("Command contained invalid characters", log_type='error')
                cmd_parse = None
            if not cmd_parse:
                continue

            # Special case for exit commands.
            if cmd_parse[0].upper() in ["EXIT", "QUIT", "Q"]:
                break

            # Dispatch the parsed command and break on False.
            if not self.dispatch(cmd_parse):
                break

        # Perform cleanup.
        self.context.save_data()
        log("Exiting...", log_type='info')

    def dispatch(self, cmd_parse: list) -> bool:
        """
        Brief:
            This function dispatches a command to its appropriate command
            handler.

        Arguments:
            cmd_parse: list
                The parsed command to dispatch.

        Returns:
            False to exit the program, True otherwise.
        """
        # Resolve command shortening within the base command.
        cmd = cmd_parse[0]
        cmd_matches = [c for c in self.command_dict if c.startswith(cmd)]

        if len(cmd_matches) == 1:
            cmd = cmd_matches[0]

        if len(cmd_matches) > 1:
            log(f"Ambiguous command: '{cmd}'. Potential matches:", log_type='error')
            for m in cmd_matches:
                log(f"   {m}")
            return True

        # Get the associated command class.
        command_class = self.command_dict.get(cmd)
        if command_class is None:
            log(f"Unknown command: '{cmd}'", log_type='error')
            return True

        # Run the command and return the boolean status.
        return command_class.run(cmd_parse[1:], self.context, self.cmd_tree)
    
    def _build_cmd_tree(self) -> CommandNode:
        """
        Brief:
            This function builds the command tree used for autocompletion
            and command shortening.
        """
        # Create the root node with blank data.
        root = CommandNode("")

        # Fill the tree with each command class in the dict.
        for command_class in self.command_dict.values():
            node = command_class.create_cmd_tree()
            root.children.append(node)

        return root

###   end of file   ###
