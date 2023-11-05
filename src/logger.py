"""
file: src/logger.py

This file contains the logger functionality for printing
to standard out and standard error in a standardized way.
"""

import emoji

def _emoji_check():
    """
    Brief:
        This is a helper function to determine if the current
        environment can display emojis.

    Returns:
        True or False.
    """
    try:
        emoji.emojize(":thumbs_up:")
    except UnicodeEncodeError:
        return False
    
    return True

def log(msg, log_type='blank', end="\n"):
    """
    Brief:
        This function logs a message with the specified log type.

    Arguments:
        msg: str
            The message to log.
        log_type: str, optional (default: 'info')
            The type of log message.
    """
    emoji_status = _emoji_check()

    log_symbols = {
        'info': '🐝' if emoji_status else '+',
        'success': '✅' if emoji_status else '*',
        'error': '🛑' if emoji_status else '!',
        'warning': '❓' if emoji_status else '?',
        'cookie': '🍪' if emoji_status else '+',
    }

    sym = log_symbols.get(log_type)
    if sym is not None:
        print(f"[{log_symbols.get(log_type, '🐝')}] ", end="")
    print(f"{msg}", end=end)

###   end of file   ###
