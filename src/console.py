"""
file: src/console.py

This file contains the class definitions for the console suite.
"""

import os
import getch
import shlex
import sys
import yaml

from src.node import CommandNode
from src.logger import log

from src.command.command_interface import CommandInterface

# Key macros.
ESC_SEQUENCE = '\x1b'
KEY_BACKSPACE = '\x7f'

# The default length for the command history.
DEFAULT_HISTORY_LEN = 20

# The max length of a command.
DEFAULT_MAX_CMD_LEN = 1024

def lcp(l: list) -> str:
    """
    Brief:
        This is a helper function to find the longest common prefix
        of a list of strings.
    """
    if not l:
        return ""
    
    min_l = min(len(s) for s in l)

    for i in range(min_l):
        if not all(s[i] == l[0][i] for s in l):
            return l[0][:i]
        
    return l[0][:min_l]

class Console:
    """
    Brief:
        This class defines a console. It's job is to prompt the user
        for commands as well as track and save history.

        It uses the cmd_tree to perform autocompletions and command
        shortening.
    """
    def __init__(self, history_file: str=None, cmd_tree: CommandNode=None):
        self.history = []
        self.max_history_len = DEFAULT_HISTORY_LEN
        self.max_cmd_len = DEFAULT_MAX_CMD_LEN

        # Private members for tracking command prompting.
        self.cmd_idx = 0
        self.hist_idx = 0
        self.cmd = ""
        self.saved_cmd = ""

        # This holds the root node for the command tree, used in autocomp.
        self.cmd_tree = cmd_tree

        # Attempt to load history.
        self.history_file = history_file
        self._load_history()

    def prompt(self) -> str:
        """
        Brief:
            This function is the client-facing prompt, which uses the
            private _prompt function to gather a command, updates both
            local and persistent history, then returns the command.

        Returns:
            The user-issued command.
        """
        # Prompt the user for a command.
        try:
            cmd = self._prompt()
        except KeyboardInterrupt:
            # Re-raise to propagate.
            raise

        # Strip the command.
        if cmd is not None:
            cmd = cmd.strip()

        # If this command matches the last entered command, don't push
        # to history.
        if len(self.history) > 0 and self.history[0] == cmd:
            return cmd
        
        # Add command to history.
        self.history.insert(0, cmd)
        if len(self.history) > self.max_history_len:
            self.history.pop()

        # Add command to persistent history file.
        # This fails silently.
        self._write_history(cmd)

        return cmd

    def _prompt(self) -> str:
        """
        Brief:
            This function prompts the user for a command and returns
            when the user presses enter.

            Up and down arrow presses for history seeking.

            Tab completions are performed with the command tree.

            Command shortening also leverages the command tree.
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

            # Tab Completions.
            if inp == "\t":
                parse = shlex.split(self.cmd)
                if len(self.cmd) > 0 and self.cmd[len(self.cmd) - 1] == " " and self.cmd_idx == len(self.cmd):
                    parse.append("")
                cur_node = self.cmd_tree

                # Check for empty command.
                if parse is None or len(parse) == 0:
                    continue

                for token in parse:
                    match_nodes = [c for c in cur_node.children if c.name.startswith(token)]

                    # Check for no matches.
                    if not match_nodes:
                        break

                    # Traverse the tree.
                    cur_node = match_nodes[0]

                # If there are no matches returned, do nothing.
                if not match_nodes:
                    continue

                # If there is only one match returned, we can autofill.
                if len(match_nodes) == 1:
                    parse[len(parse) - 1] = match_nodes[0].name
                    for _ in range(self.cmd_idx):
                        print("\b", end="")
                    self.cmd = shlex.join(parse) + " "
                    self.cmd_idx = len(self.cmd)
                    print(self.cmd, end="")
                    continue

                # If there are multiple matches, list them.
                print("")
                for node in match_nodes:
                    print(node.name, end="\t")

                # We can now find the longest common prefix and
                # auto-fill that.
                match_names = [node.name for node in match_nodes]
                fill = lcp(match_names)
                if len(fill) > 0:
                    parse[len(parse) - 1] = lcp(match_names)
                    self.cmd = shlex.join(parse)
                self.cmd_idx = len(self.cmd)
                print(f"\n> {self.cmd}", end="")
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

    def _load_history(self):
        """
        Brief:
            This function attempts to load the command history from
            the persistent history file.

            If the history file does not exist, it attempts to create an
            empty one.
        """
        # Check if history file exists.
        if not os.path.exists(self.history_file):
            self._create_history_file()
            return

        # Open file and read in data.
        try:
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
            return

        log("Restored previous session history", log_type='success')

    def _create_history_file(self) -> bool:
        """
        Brief:
            This function attempts to create a new history file.

        Returns:
            True on success, False on error.
        """
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                pass
        except OSError:
            log(
                f"Unable to create history file at '{self.history_file}'",
                log_type='error',
            )
            return False
        return True

    def _write_history(self, cmd: str):
        """
        Brief:
            This function attempts to write a command to the history file.

        Arguments:
            cmd: str
                The command to write.
        """
        # Check if the history file exists.
        if not os.path.exists(self.history_file):
            if not self._create_history_file():
                # Fail silently.
                return

        # Append command to history file.
        try:
            with open(self.history_file, 'a', encoding='utf-8') as f:
                f.write(cmd + '\n')
        except OSError:
            # Fail silently.
            return

###   end of file   ###
        