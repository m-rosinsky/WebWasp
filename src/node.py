"""
File:
    src/node.py

Brief:
    This file contains the class information for a command node,
    used in formation of the command syntax tree.
"""

class CommandNode():
    """
    Brief:
        This class contains the command node, which holds
        child nodes of subcommands, as well as the name of
        the command itself.
    """
    def __init__(self, name):
        self.name = name
        self.children = []

###   end of file   ###
