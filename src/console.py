"""
file: src/console.py

This file contains the class definitions for the console suite.
"""

import sys

ESC_SEQUENCE = '\x1b'

try:
    import getch
except ImportError:
    print("Run setup.py to install dependencies...")
    sys.exit(1)

class Console:
    """
    This class defines a console context.

    Members:
    -------
    is_running - The console is running.
    history - An array of previous commands.
    max_history_len - The maximum number of previous commands to store.
    """

    def __init__(self):
        self.is_running = False
        self.history = []
        self.max_history_len = 20

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

    # Private member functions.
    def _prompt(self):
        """
        This function prompts the user for input and returns
        the command.

        It handles arrow-key presses for history.
        """
        cmd = ""
        saved_cmd = ""
        hist_idx = -1
        print("> ", end="")
        
        while True:
            sys.stdout.flush()

            try:
                inp = getch.getch()
            except (OverflowError, KeyboardInterrupt):
                self.is_running = False
                break
            
            if inp == ESC_SEQUENCE:
                esc_seq = getch.getch() + getch.getch()

                if esc_seq == '[A': # UP ARROW
                    # Upper bound check.
                    if hist_idx + 1 >= len(self.history):
                        continue

                    hist_idx += 1
                    
                    # Create a save of current command buffer if this
                    # is the first up arrow press.
                    if hist_idx == 0:
                        saved_cmd = cmd

                    # Blank line and return cursor.
                    for _ in range(len(cmd)):
                        print("\b", end="")
                        print(" ", end="")
                        print("\b", end="")

                    # Retreive historical command.
                    cmd = self.history[hist_idx]

                    # Print command
                    print(cmd, end="")
                    continue

                if esc_seq == '[B': # DOWN ARROW
                    # Lower bound check.
                    if hist_idx == -1:
                        continue
                    
                    hist_idx -= 1

                    # Blank line and return cursor.
                    for _ in range(len(cmd)):
                        print("\b", end="")
                        print(" ", end="")
                        print("\b", end="")

                    # Get either saved command or historical command.
                    if hist_idx == -1:
                        cmd = saved_cmd
                    else:
                        cmd = self.history[hist_idx]

                    # Print command.
                    print(cmd, end="")
                    continue

                continue

            # Return.
            if inp == "\n":
                print("")
                break
            
            # Normal input.
            cmd += inp
            print(inp, end="")
        return cmd

###   end of file   ###
        