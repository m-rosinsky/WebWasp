"""
file: src/console.py

This file contains the class definitions for the console suite.
"""

import os
import getch
import sys
import yaml

from src import dispatch
from src.logger import log
from src.response import Response
from src.headers import Headers

ESC_SEQUENCE = '\x1b'
KEY_BACKSPACE = '\x7f'

class Console:
    """
    This class defines a console context.

    Members:
    -------
    is_running      - The console is running.
    history         - An array of previous commands.
    max_history_len - The maximum number of previous commands to store.
    max_self.cmd_len     - The maximum size of a command being entered.

    vars            - The vars held by the console.
    """

    def __init__(self):
        self.is_running = False
        self.history = []
        self.max_history_len = 20
        self.max_cmd_len = 1024

        self.vars = {}

        # Private members for tracking command prompting.
        self.cmd_idx = 0
        self.hist_idx = 0
        self.cmd = ""
        self.saved_cmd = ""

        # This class holds the most recent response information.
        self.response = Response()
        self.has_response = False

        # This holds the timeout value for requests (seconds).
        self.timeout_s = 2

        # This holds the request parameters.
        self.params = {}

        # This holds the request cookies.
        self.cookies = {}

        # This holds the request headers.
        self.headers = Headers()

        # Attempt to load exported variables.
        self.data_file = os.path.expanduser("~/.wwdata")
        self._load_data()

        # Attempt to load history.
        self.history_file = os.path.expanduser("~/.wwhistory")
        self._load_history()

    def run(self):
        """
        This function runs the console suite.

        The function accepts input, parses the command, and performs
        the appropriate execution.
        """
        self.is_running = True

        while self.is_running:
            # Get input.
            try:
                cmd = self._prompt()
            except KeyboardInterrupt:
                print("^C")
                self.is_running = False
                break

            # Add input to history.
            self.history.insert(0, cmd)
            if len(self.history) > self.max_history_len:
                self.history.pop()
            
            # Add input to persistent file.
            try:
                if not os.path.exists(self.history_file):
                    with open(self.history_file, 'w', encoding='utf-8') as f:
                        f.write(cmd + "\n")
                else:
                    with open(self.history_file, 'a', encoding='utf-8') as f:
                        f.write(cmd + "\n")
            except OSError:
                log(
                    "Unable to store session command history",
                    log_type='warning',
                )

            # Handle command.
            status = dispatch.dispatch(cmd, self.vars, self)

            if not status:
                self.is_running = False

        # Save all persistent data for session.
        self.update_data()

    def update_data(self):
        """
        Brief:
            This function updates the persistent data file with the
            data stored in the console variables.
        """
        # Check if the persistent data file does not exist.
        if not os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'w+', encoding='utf-8') as f:
                    pass
            except OSError:
                log("Unable to create persistent data file", log_type='error')
                return
            
        yaml_data = {
            'cookies': {},
            'params': {},
            'var': {},
        }

        # Add cookies.
        for name, value in self.cookies.items():
            yaml_data['cookies'][name] = value

        # Add parameters.
        for name, value in self.params.items():
            yaml_data['params'][name] = value

        # Add variables.
        for name, value in self.vars.items():
            yaml_data['var'][name] = value

        # Dump the contents back to the data file.
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                yaml.dump(yaml_data, f, default_flow_style=False)
        except (OSError, yaml.YAMLError, AttributeError):
            log("Unable to write to persistent data file", log_type='error')
            return

    # Private member functions.
    def _load_data(self):
        """
        This function attempts to populate the vars member via
        the saved export file if it exists.
        """
        # Check if the data file exists.
        if not os.path.exists(self.data_file):
            return
        
        # Read the file data.
        file_data = ""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                for line in f:
                    file_data += line
        except OSError:
            log("Unable to read persistent data file", log_type='error')
            return
        
        # Parse the file data as YAML.
        yaml_data = yaml.safe_load(file_data) or {}
        
        # Load sections into console variables.
        if 'cookies' in yaml_data:
            self.cookies = yaml_data['cookies']
        if 'params' in yaml_data:
            self.params = yaml_data['params']
        if 'var' in yaml_data:
            self.vars = yaml_data['var']

    def _load_history(self):
        """
        This function attempt to read the history command file
        in order to restore history from previous sessions.
        """
        try:
            if not os.path.exists(self.history_file):
                return

            # Open file and read in data.
            with open(self.history_file, 'r', encoding='utf-8') as f:
                for line in f:
                    self.history.insert(0, line.strip())
                    if len(self.history) > self.max_history_len:
                        self.history.pop()

        except OSError as imp_err:
            log(
                "Warning: Could not restore session history",
                log_type='warning',
            )
            log(f"   {imp_err}")

        log("Restored previous session history", log_type='success')

    def _prompt(self):
        """
        This function prompts the user for input and returns
        the command.

        It handles arrow-key presses for history.
        """

        # This stores the current command.
        self.cmd = ""

        # This stores the current position within the buffer, which
        # is useful with left and right arrow seeking.
        self.cmd_idx = 0

        # This saves a command buffer when the up arrow is used to
        # retreive history.
        self.saved_cmd = ""

        # This tracks which historical command to pull.
        self.hist_idx = -1

        # Display prompt.
        print("> ", end="")

        while True:
            sys.stdout.flush()

            try:
                inp = getch.getch()
            except OverflowError: # Catch non-ascii characters.
                continue
            except KeyboardInterrupt:
                self.is_running = False
                break

            if inp == ESC_SEQUENCE:
                self._prompt_esc_seq()
                continue

            # Backspace.
            if inp == KEY_BACKSPACE:
                # Bounds check.
                if self.cmd_idx == 0:
                    continue

                # Move cursor back one.
                print("\b", end="")

                # Print all following characters.
                for i in range(self.cmd_idx, len(self.cmd)):
                    print(self.cmd[i], end="")

                # Print a space at end.
                print(" ", end="")

                # Return cursor.
                for _ in range(self.cmd_idx, len(self.cmd)):
                    print("\b", end="")
                print("\b", end="")

                self.cmd_idx -= 1

                # Slice string.
                self.cmd = self.cmd[:self.cmd_idx] + self.cmd[self.cmd_idx+1:]

                continue

            # Return.
            if inp == "\n":
                print("")
                break

            # Bound check.
            if len(self.cmd) >= self.max_cmd_len:
                continue

            # Print the character.
            print(inp, end="")

            # Insert character into self.cmd buffer.
            self.cmd = self.cmd[:self.cmd_idx] + inp + self.cmd[self.cmd_idx:]
            self.cmd_idx += 1

            # Print all characters that follow in buffer.
            for i in range(self.cmd_idx, len(self.cmd)):
                print(self.cmd[i], end="")

            # Return cursor to start position.
            for i in range(self.cmd_idx, len(self.cmd)):
                print("\b", end="")

        return self.cmd

    def _prompt_esc_seq(self):
        esc_seq = getch.getch() + getch.getch()

        if esc_seq == '[A': # UP ARROW
            # Upper bound check.
            if self.hist_idx + 1 >= len(self.history):
                return

            self.hist_idx += 1

            # Create a save of current command buffer if this
            # is the first up arrow press.
            if self.hist_idx == 0:
                self.saved_cmd = self.cmd

            # Put cursor at end of line.
            for _ in range(self.cmd_idx, len(self.cmd)):
                print(" ", end="")

            # Blank line and return cursor to beginning.
            for _ in range(len(self.cmd)):
                print("\b", end="")
                print(" ", end="")
                print("\b", end="")

            # Retreive historical command.
            self.cmd = self.history[self.hist_idx]
            self.cmd_idx = len(self.cmd)

            # Print command
            print(self.cmd, end="")

        elif esc_seq == '[B': # DOWN ARROW
            # Lower bound check.
            if self.hist_idx == -1:
                return

            self.hist_idx -= 1

            # Put cursor at end of line.
            for _ in range(self.cmd_idx, len(self.cmd)):
                print(" ", end="")

            # Blank line and return cursor.
            for _ in range(len(self.cmd)):
                print("\b", end="")
                print(" ", end="")
                print("\b", end="")

            # Get either saved command or historical command.
            if self.hist_idx == -1:
                self.cmd = self.saved_cmd
            else:
                self.cmd = self.history[self.hist_idx]

            self.cmd_idx = len(self.cmd)

            # Print command.
            print(self.cmd, end="")

        elif esc_seq == '[C': # RIGHT ARROW
            # Upper bounds check.
            if self.cmd_idx >= len(self.cmd):
                return

            print(self.cmd[self.cmd_idx], end="")
            sys.stdout.flush()
            self.cmd_idx += 1

        elif esc_seq == '[D': # LEFT ARROW
            # Lower bounds check.
            if self.cmd_idx == 0:
                return

            print("\b", end="")
            self.cmd_idx -= 1

        return

###   end of file   ###
        