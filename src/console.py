"""
file: src/console.py

This file contains the class definitions for the console suite.
"""

import sys
from src import dispatch

ESC_SEQUENCE = '\x1b'
KEY_BACKSPACE = '\x7f'

try:
    import getch
except ImportError:
    print("[🛑] Error: Missing Dependencies. ")
    print("[🛑] Run python3 -m pip install -r requirements.txt")
    sys.exit(1)

class Console:
    """
    This class defines a console context.

    Members:
    -------
    is_running      - The console is running.
    history         - An array of previous commands.
    max_history_len - The maximum number of previous commands to store.
    max_self.cmd_len     - The maximum size of a command being entered.
    """

    def __init__(self):
        self.is_running = False
        self.history = []
        self.max_history_len = 20
        self.max_cmd_len = 1024

        # Private members for tracking command prompting.
        self.cmd_idx = 0
        self.hist_idx = 0
        self.cmd = ""
        self.saved_cmd = ""

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

            # Handle command.
            status = dispatch.dispatch(cmd)

            if not status:
                self.is_running = False

    # Private member functions.
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
        