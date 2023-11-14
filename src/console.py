"""
file: src/console.py

This file contains the class definitions for the console suite.
"""

import os
import getch
import shlex
import sys
import yaml

from src import dispatch
from src.node import CommandNode
from src.logger import log
from src.response import Response
from src.headers import Headers

from src.command.command_interface import CommandInterface

ESC_SEQUENCE = '\x1b'
KEY_BACKSPACE = '\x7f'

DEFAULT_SESSION_NAME = 'default'

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

        # Private members for tracking command prompting.
        self.cmd_idx = 0
        self.hist_idx = 0
        self.cmd = ""
        self.saved_cmd = ""

        # This holds the current console session name.
        self.cur_session = DEFAULT_SESSION_NAME

        # This holds the root node for the command tree, used in autocomp.
        self.cmd_root = CommandNode("")
        self._load_cmd_tree()

        # This class holds the most recent response information.
        self.response = Response()
        self.has_response = False

        # This holds the timeout value for requests (seconds).
        self.timeout_s = 2

        # This holds the console variables.
        self.vars = {}

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
            status = dispatch.dispatch(cmd, self)

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
            self.cur_session: {
                'cookies': {},
                'headers': {
                    'auth': {},
                    'fields': {},
                },
                'params': {},
                'var': {},
                'timeout': self.timeout_s,
            },
        }

        # Add current session.
        yaml_data['cur_session'] = self.cur_session

        # Add cookies.
        for name, value in self.cookies.items():
            yaml_data[self.cur_session]['cookies'][name] = value

        # Add headers.
        for name, value in self.headers.auth.items():
            yaml_data[self.cur_session]['headers']['auth'][name] = value
        for name, value in self.headers.fields.items():
            yaml_data[self.cur_session]['headers']['fields'][name] = value

        # Add parameters.
        for name, value in self.params.items():
            yaml_data[self.cur_session]['params'][name] = value

        # Add variables.
        for name, value in self.vars.items():
            yaml_data[self.cur_session]['var'][name] = value

        # Dump the contents back to the data file.
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                yaml.dump(yaml_data, f, default_flow_style=False)
        except (OSError, yaml.YAMLError, AttributeError):
            log("Unable to write to persistent data file", log_type='error')
            return

    # Private member functions.
    def _load_cmd_tree(self):
        """
        Brief:
            This function loads the command syntax tree from the
            base commands located in the dispatch module.
        """
        # Iterate through all base command classes in the command dict.
        for name, command_class in dispatch.command_dict.items():
            if not isinstance(command_class, CommandInterface):
                node = CommandNode(name)
            else:
                node = command_class.create_cmd_tree()
            self.cmd_root.children.append(node)

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
        
        # Load current session tag.
        if 'cur_session' in yaml_data:
            self.cur_session = yaml_data['cur_session']

        # Load sections into console variables from current session.
        if self.cur_session not in yaml_data:
            log(f"Unable to load data for session '{self.cur_session}'...", log_type='error')
            log("Creating new session...")
            return
        
        cur_session_data = yaml_data[self.cur_session]
        if 'cookies' in cur_session_data:
            self.cookies = cur_session_data['cookies']
        if 'headers' in cur_session_data:
            if 'auth' in cur_session_data['headers']:
                self.headers.auth = cur_session_data['headers']['auth']
            if 'fields' in cur_session_data['headers']:
                self.headers.fields = cur_session_data['headers']['fields']
        if 'params' in cur_session_data:
            self.params = cur_session_data['params']
        if 'var' in cur_session_data:
            self.vars = cur_session_data['var']
        if 'timeout' in cur_session_data:
            self.timeout_s = cur_session_data['timeout']

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

            # Tab Completions.
            if inp == "\t":
                parse = shlex.split(self.cmd)
                if len(self.cmd) > 0 and self.cmd[len(self.cmd) - 1] == " " and self.cmd_idx == len(self.cmd):
                    parse.append("")
                cur_node = self.cmd_root

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

###   end of file   ###
        