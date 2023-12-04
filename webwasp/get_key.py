"""
File:
    src/get_key.py

Brief:
    This file is responsible for handling single-key presses and
    returning a key code pressed, so it may be handled by the console.

    This module needs to be as cross-platform as possible.
"""

import platform
import readchar
from enum import Enum

class Key(Enum):
    UP = 1,
    DOWN = 2,
    LEFT = 3,
    RIGHT = 4,
    RETURN = 5,
    TAB = 6,
    BACKSPACE = 7,
    CTRL_C = 8,

class Platforms(Enum):
    WIN = 1,
    UNIX = 2,

# Get platform string.
_PLATFORM = Platforms.WIN if "Windows" in platform.platform() else Platforms.UNIX

def get_key():
    """
    Brief:
        This function gets a single key press from stdin
         
    Returns:
        A string representing the alphanumeric key, or a
        Key from the Key enum for more complex escape sequences.
    """
    # Use readchar to get the key.
    k = readchar.readchar()
    ord_k = ord(k)

    # No platform dependence for CTRL_C.
    if k == readchar.key.CTRL_C:
        return Key.CTRL_C
    
    # Return:
    if _PLATFORM == Platforms.WIN and ord_k == 0x0d:
        return Key.RETURN
    if _PLATFORM == Platforms.UNIX and ord_k == 0x0a:
        return Key.RETURN
    
    # Backspace:
    if _PLATFORM == Platforms.WIN and ord_k == 0x08:
        return Key.BACKSPACE
    if _PLATFORM == Platforms.UNIX and ord_k == 0x7f:
        return Key.BACKSPACE
    
    # Tab:
    if ord_k == 0x09:
        return Key.TAB
    
    # Escape sequences.
    if _PLATFORM == Platforms.WIN and (ord_k == 0xe0 or ord_k == 0x00):
        # Windows escape sequences are 2 character sequences.
        k2 = readchar.readchar()
        k2_ord = ord(k2)
        if k2_ord == 0x48:
            return Key.UP
        if k2_ord == 0x50:
            return Key.DOWN
        if k2_ord == 0x4b:
            return Key.LEFT
        if k2_ord == 0x4d:
            return Key.RIGHT
        
        return None
        
    if _PLATFORM == Platforms.UNIX and ord_k == 0x1b:
        # Unix escape sequences are 3 character sequences.
        k2 = readchar.readchar()
        k3 = readchar.readchar()
        k2_ord = ord(k2)
        k3_ord = ord(k3)

        # The second character in the sequence must be this value.
        if k2_ord != 0x5b:
            return None
        
        if k3_ord == 0x41:
            return Key.UP
        if k3_ord == 0x42:
            return Key.DOWN
        if k3_ord == 0x43:
            return Key.RIGHT
        if k3_ord == 0x44:
            return Key.LEFT
        return None

    return k
