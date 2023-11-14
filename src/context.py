"""
File:
    src/context.py

Brief:
    This file contains the context class.
"""

import os
import yaml

from src.response import Response
from src.headers import Headers
from src.logger import log

# The default request timeout value in seconds.
DEFAULT_TIMEOUT = 2.0

# The default name for a session.
DEFAULT_SESSION_NAME = 'default'

class Context:
    """
    Brief:
        This class contains a context for the current WebWasp session.
    """
    def __init__(self, filename: str=None):
        # The current session name.
        self.cur_session = DEFAULT_SESSION_NAME
        
        # The request timeout value.
        self.timeout = DEFAULT_TIMEOUT

        # This class holds the most recent response information.
        self.response = Response()
        self.has_response = False

        # This holds the request headers.
        self.headers = Headers()

        # This holds the console variables.
        self.vars = {}

        # This holds the request parameters.
        self.params = {}

        # This holds the request cookies.
        self.cookies = {}

        # Persistent data file.
        self.data_file = filename
        self._load_data()

    def reset_data(self):
        """
        Brief:
            This function resets the context data to its defaults.
        """
        self.timeout = DEFAULT_TIMEOUT
        self.headers = Headers()
        self.vars = {}
        self.params = {}
        self.cookies = {}

    def print_session_list(self):
        """
        Brief:
            This function prints the names of all currently stored sessions
            in the persistent file.
        """
        if not os.path.exists(self.data_file):
            return
        
        yaml_data = self._read_data()
        if yaml_data is None:
            log("Failed to read data file", log_type='error')
            return

        for name in yaml_data.keys():
            if name == 'cur_session':
                continue
            if name == self.cur_session:
                log(f"   \033[32m{name} *\033[0m")
            else:
                log(f"   {name}")

    def new_session(self, name: str) -> bool:
        """
        Brief:
            This function adds a new session with a given name.
            
        Returns: bool
            If the session already exists, this returns False.

            Otherwise returns True.
        """
        # Check if the session already exists.
        if self._find_session(name) is not None:
            return False
        
        # Save the current session data.
        self.save_data()

        # Change the session name.
        self.cur_session = name

        # Reset the local variables.
        self.reset_data()

        # Save the session into the file.
        self.save_data()

        return True

    def save_data(self):
        """
        Brief:
            This function saves the current session data into the persistent
            data file.
        """
        # If the data file does not exist, create a blank one.
        if not os.path.exists(self.data_file):
            if not self._create_data_file():
                return
            
        # Create the session data.
        session_data = {
            'cookies': self.cookies,
            'headers': {
                'auth': self.headers.auth,
                'fields': self.headers.fields,
            },
            'params': self.params,
            'vars': self.vars,
            'timeout': self.timeout,
        }

        # Read the YAML data.
        yaml_data = self._read_data()
        if yaml_data is None:
            log("Failed to save session data", log_type='error')
            return
        
        # Save the data in the YAML.
        yaml_data['cur_session'] = self.cur_session
        yaml_data[self.cur_session] = session_data

        # Open the data file for writing.
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                # Write the YAML back to the file.
                yaml.dump(yaml_data, f, default_flow_style=False)
        except [OSError, yaml.YAMLError, AttributeError]:
            log("Failed to save session data", log_type='error')
            return

    def _read_data(self) -> dict:
        """
        Brief:
            This function reads the data into a YAML dictionary.

        Returns: dict
            The dictionary containing all persistent file data.

            None on error.
        """
        if not os.path.exists(self.data_file):
            return None
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                # Read the data file.
                file_data = ""
                for line in f:
                    file_data += line

                yaml_data = yaml.safe_load(file_data) or {}
        except [OSError, yaml.YAMLError, AttributeError]:
            return None

        return yaml_data

    def _load_data(self) -> bool:
        """
        Brief:
            This function attempts to load the data associated with the
            current session.

            If the persistent file does not exist, it will create a blank one.

            If the cur_session does not exist, it will switch to default.
        """
        if not os.path.exists(self.data_file):
            if not self._create_data_file():
                log("Failed to create persistent data file", log_type='error')
            self.save_data()
            return
        
        # Read the data file.
        yaml_data = self._read_data()
        if yaml_data is None:
            return False
        
        # Store the value in the cur session tag as the current session.
        # If it does not exist, store the default session.
        self.cur_session = yaml_data.get('cur_session', DEFAULT_SESSION_NAME)

        # If the session does not exist, create it.
        if self.cur_session not in yaml_data:
            if not self.save_data():
                return False
            return True
        
        # If the session does exist, load its values into the context variables.
        if 'cookies' in yaml_data[self.cur_session]:
            self.cookies = yaml_data[self.cur_session]['cookies']
        if 'params' in yaml_data[self.cur_session]:
            self.params = yaml_data[self.cur_session]['params']
        if 'vars' in yaml_data[self.cur_session]:
            self.vars = yaml_data[self.cur_session]['vars']
        if 'timeout' in yaml_data[self.cur_session]:
            self.timeout = yaml_data[self.cur_session]['timeout']
        if 'headers' in yaml_data[self.cur_session]:
            if 'auth' in yaml_data[self.cur_session]['headers']:
                self.headers.auth = yaml_data[self.cur_session]['headers']['auth']
            if 'fields' in yaml_data[self.cur_session]['headers']:
                self.headers.fields = yaml_data[self.cur_session]['headers']['fields']

    def _create_data_file(self) -> bool:
        """
        Brief:
            This function attempts to create the persistent data file.

        Returns: bool
            True on success, False on error.
        """
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                pass
        except OSError:
            return False
        return True

    def _find_session(self, name: str) -> dict:
        """
        Brief:
            This function finds a session with a given name within the
            persistent data file.

        Arguments:
            name: str
                The name of the session to find.

        Returns:
            A dictionary containing the session data, or None if it does
            not exist.
        """
        if not os.path.exists(self.data_file):
            return None
        
        # Get the yaml for the session data.
        file_data = ""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                for line in f:
                    file_data += line
        except OSError:
            return None

        yaml_data = yaml.safe_load(file_data) or {}

        return yaml_data.get(name)

###   end of file   ###
