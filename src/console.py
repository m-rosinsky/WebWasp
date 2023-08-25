"""
file: src/console.py

This file contains the class definitions for the console suite.
"""

import sys

ESC_SEQUENCE = '\x1b'
KEY_BACKSPACE = '\x7f'

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
    is_running      - The console is running.
    history         - An array of previous commands.
    max_history_len - The maximum number of previous commands to store.
    max_cmd_len     - The maximum size of a command being entered.
    """

    def __init__(self):
        self.is_running = False
        self.history = []
        self.max_history_len = 20
        self.max_cmd_len = 1024

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

        # This stores the current command.
        cmd = ""

        # This stores the current position within the buffer, which
        # is useful with left and right arrow seeking.
        cmd_idx = 0

        # This saves a command buffer when the up arrow is used to
        # retreive history.
        saved_cmd = ""

        # This tracks which historical command to pull.
        hist_idx = -1

        # Display prompt.
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

                    # Put cursor at end of line.
                    for _ in range(cmd_idx, len(cmd)):
                        print(" ", end="")

                    # Blank line and return cursor to beginning.
                    for _ in range(len(cmd)):
                        print("\b", end="")
                        print(" ", end="")
                        print("\b", end="")

                    # Retreive historical command.
                    cmd = self.history[hist_idx]
                    cmd_idx = len(cmd)

                    # Print command
                    print(cmd, end="")
                    continue

                if esc_seq == '[B': # DOWN ARROW
                    # Lower bound check.
                    if hist_idx == -1:
                        continue
                    
                    hist_idx -= 1

                    # Put cursor at end of line.
                    for _ in range(cmd_idx, len(cmd)):
                        print(" ", end="")

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

                    cmd_idx = len(cmd)

                    # Print command.
                    print(cmd, end="")
                    continue

                if esc_seq == '[C': # RIGHT ARROW
                    # Upper bounds check.
                    if cmd_idx >= len(cmd):
                        continue

                    print(cmd[cmd_idx], end="")
                    sys.stdout.flush()
                    cmd_idx += 1
                    continue

                if esc_seq == '[D': # LEFT ARROW
                    # Lower bounds check.
                    if cmd_idx == 0:
                        continue

                    print("\b", end="")
                    cmd_idx -= 1
                    continue

                continue

            # Backspace.
            if inp == KEY_BACKSPACE:
                # Bounds check.
                if cmd_idx == 0:
                    continue

                # Move cursor back one.
                print("\b", end="")

                # Print all following characters.
                for i in range(cmd_idx, len(cmd)):
                    print(cmd[i], end="")

                # Print a space at end.
                print(" ", end="")

                # Return cursor.
                for _ in range(cmd_idx, len(cmd)):
                    print("\b", end="")
                print("\b", end="")

                cmd_idx -= 1

                # Slice string.
                cmd = cmd[:cmd_idx] + cmd[cmd_idx+1:]

                continue

            # Return.
            if inp == "\n":
                print("")
                break
            
            # Bound check.
            if len(cmd) >= self.max_cmd_len:
                continue

            # Print the character.
            print(inp, end="")

            # Insert character into cmd buffer.
            cmd = cmd[:cmd_idx] + inp + cmd[cmd_idx:]
            cmd_idx += 1

            # Print all characters that follow in buffer.
            for i in range(cmd_idx, len(cmd)):
                print(cmd[i], end="")

            # Return cursor to start position.
            for i in range(cmd_idx, len(cmd)):
                print("\b", end="")

        return cmd

###   end of file   ###
        