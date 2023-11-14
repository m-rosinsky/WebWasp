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
from src.logger import log
from src.node import CommandNode

from src.command.command_clear import CommandClear

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
        # The current session context.
        self.context = None

        # The history and data files.
        self.history_file = os.path.expanduser(HISTORY_FILE)
        self.data_file = os.path.expanduser(DATA_FILE)

        # Form the command autocomp tree.
        self.cmd_tree = CommandNode("")

        # The console object, using the history file to track command history.
        self.console = Console(history_file=self.history_file)

        # The command dictionary, consisting of all command classes and
        # the associated command names.
        self.command_dict = {
            'clear': CommandClear('clear'),
        }

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
            cmd_parse = shlex.split(cmd)

            # Special case for exit commands.
            if cmd_parse[0].upper() in ["EXIT", "QUIT", "Q"]:
                break

            # Dispatch the parsed command, and break on False.
            if not self.dispatch(cmd_parse):
                break

        # Perform cleanup.
        print("Exiting...")

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
        # Resolve command shortening with the command tree.

        # Get the associated command class.
        command_class = self.command_dict.get(cmd_parse[0])
        if command_class is None:
            log(f"Unknown command: '{cmd_parse[0]}'", log_type='error')

        # Run the command and return the boolean status.
        return command_class.run(cmd_parse[1:], self.context)

###   end of file   ###
