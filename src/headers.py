"""
file: src/headers.py

This file contains the headers class, which is leveraged
by the console to store request header information.
"""

class Headers():
    """
    This class contains a dictionary that holds predefined header
    field names that are sent along with requests.

    It also contains the auth field which can be used
    to authenticate into 403 protected urls.
    """
    def __init__(self):
        self.fields = {
            "user-agent" : None,
        }
        self.auth = {
            "auth-user" : None,
            "auth-pass" : None
        }

    def print_fields(self):
        """
        This function lists the header fields.
        """
        for field, value in self.auth.items():
            print(f"   {field}\t: ", end="")
            if value is None:
                value = "''"
            print(f"{value}")

        for field, value in self.fields.items():
            print(f"   {field}\t: ", end="")
            if value is None:
                value = "''"
            print(f"{value}")

    def field_valid(self, field):
        """
        This function returns True if the specified field is valid.
        """
        return (field in self.fields) or (field in self.auth)

    def set_field(self, field, value):
        if not self.field_valid(field):
            return
        if field in self.fields:
            self.fields[field] = value
            return
        self.auth[field] = value

    def clear_fields(self):
        for field in self.fields:
            self.fields[field] = None
        for field in self.auth:
            self.auth[field] = None

###   end of file   ###
