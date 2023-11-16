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

# The tag name for the current session.
SESSION_TAG_NAME = 'cur_session'

# This error is raised when there is an I/O error with the persistent
# data file.
class DataError(BaseException):
    pass

# This error is raised when a given session name does not exist.
class SessionNotFoundError(BaseException):
    pass

# This error is raised when a duplicate session attempts to be created.
class DupSessionError(BaseException):
    pass

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

        Raises:
            DataError on I/O errors.
        """
        self.timeout = DEFAULT_TIMEOUT
        self.headers = Headers()
        self.vars = {}
        self.params = {}
        self.cookies = {}

        try:
            self.save_data()
        except DataError:
            raise

    def print_session_list(self):
        """
        Brief:
            This function prints the names of all currently stored sessions
            in the persistent file.
        """
        if not os.path.exists(self.data_file):
            raise DataError
        
        yaml_data = self._read_data()
        if yaml_data is None:
            raise DataError

        for name in yaml_data.keys():
            if name == SESSION_TAG_NAME:
                continue
            if name == self.cur_session:
                log(f"   \033[32m{name} *\033[0m")
            else:
                log(f"   {name}")

    def new_session(self, name: str):
        """
        Brief:
            This function adds a new session with a given name.
            
        Raises:
            DupSessionError on duplicate session.
            DataError on I/O errors.
        """
        # Check if the session already exists.
        if self._find_session(name) is not None:
            raise DupSessionError
        
        # Save the current session data, reset, and save new session.
        try:
            self.save_data()
            self.cur_session = name
            self.reset_data()
            self.save_data()
        except DataError:
            raise

    def save_data(self):
        """
        Brief:
            This function saves the current session data into the persistent
            data file.
        """
        # If the data file does not exist, create a blank one.
        if not os.path.exists(self.data_file):
            try:
                self._create_data_file()
            except DataError:
                raise
            
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
            raise DataError
        
        # Save the data in the YAML.
        yaml_data[SESSION_TAG_NAME] = self.cur_session
        yaml_data[self.cur_session] = session_data

        # Open the data file for writing.
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                # Write the YAML back to the file.
                yaml.dump(yaml_data, f, default_flow_style=False)
        except [OSError, yaml.YAMLError, AttributeError]:
            raise DataError

    def load_session(self, name: str):
        """
        Brief:
            This function loads an existing session.

        Arguments:
            name: str
                The session name to load.

        Raises:
            SessionNotFoundError on name not existing as a session.
            DataError on I/O error.
        """
        # Check if the session exists.
        if self._find_session(name) is None:
            raise SessionNotFoundError
        
        # Save the current session.
        try:
            self.save_data()
            self._load_data(name)
            self.save_data()
        except DataError:
            raise

    def copy_session(self, name: str):
        """
        Brief:
            This function copies the current session to a new or existing
            session with a given name.

        Arguments:
            name: str
                The name of the session to copy data to.

        Raises:
            DataError on I/O error.
        """
        # If the named session does not exist, create a new session.
        if self._find_session(name) is None:
            try:
                self.save_data()
                self.cur_session = name
                self.save_data()
            except [DataError, DupSessionError]:
                raise
            return

        # Switch to target session.
        self.cur_session = name

        # Save the data.
        try:
            self.save_data()
        except DataError:
            raise

    def delete_session(self, name: str):
        """
        Brief:
            This function deletes a named session. If the current session has
            been deleted, the current session switches back to default.

            If default is deleted, it resets default instead of deleting.

        Arguments:
            name: str
                The name of the session to delete.

        Raises:
            SessionNotFoundError on name not existing as a session.
            DataError on I/O error.
        """
        # Check if named session exists.
        if self._find_session(name) is None:
            raise SessionNotFoundError
        
        # If we delete the active session, switch to default.
        if self.cur_session == name:
            self.load_session(DEFAULT_SESSION_NAME)

        # If the named session is the default, reset instead of delete.
        if name == DEFAULT_SESSION_NAME:
            try:
                self.reset_data()
                self.save_data()
            except DataError:
                raise
            return
        
        # Get data.
        try:
            yaml_data = self._read_data()
        except DataError:
            raise

        if yaml_data is None:
            raise DataError
                
        # Delete entry for named session.
        del yaml_data[name]

        # Dump yaml back.
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                # Write the YAML back to the file.
                yaml.dump(yaml_data, f, default_flow_style=False)
        except [OSError, yaml.YAMLError, AttributeError]:
            raise DataError
        
        # Load data from current session.
        try:
            self._load_data()
        except DataError:
            raise

    def _read_data(self) -> dict:
        """
        Brief:
            This function reads the data into a YAML dictionary.

        Returns: dict
            The dictionary containing all persistent file data.

            None on error.
        """
        if not os.path.exists(self.data_file):
            raise DataError
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                # Read the data file.
                file_data = ""
                for line in f:
                    file_data += line

                yaml_data = yaml.safe_load(file_data) or {}
        except [OSError, yaml.YAMLError, AttributeError]:
            raise DataError

        return yaml_data

    def _load_data(self, name: str=None):
        """
        Brief:
            This function attempts to load the data associated with the
            current session.

            If the persistent file does not exist, it will create a blank one.

            If the cur_session does not exist, it will switch to default.

        Arguments:
            name: str
                The name of the session to load. If None, it will attempt
                to load the session stored in the SESSION_TAG_NAME of the
                persistent file.

        Raises:
            DataError on I/O errors.
        """
        if not os.path.exists(self.data_file):
            try:
                self._create_data_file()
                self.save_data()
            except DataError:
                raise
            return
        
        # Read the data file.
        yaml_data = self._read_data()
        if yaml_data is None:
            raise DataError
        
        # Get the name of the provided session, or the SESSION_TAG_NAME if
        # None was provided.
        if name is None:
            self.cur_session = yaml_data.get(SESSION_TAG_NAME, DEFAULT_SESSION_NAME)
        else:
            self.cur_session = name

        # If the session does not exist, create it.
        if self.cur_session not in yaml_data:
            try:
                self.save_data()
            except DataError:
                raise
        
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

    def _create_data_file(self):
        """
        Brief:
            This function attempts to create the persistent data file.

        Raises:
            DataError if there is an error creating the file.
        """
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                pass
        except OSError:
            raise DataError

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
