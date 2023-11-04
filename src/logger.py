"""
file: src/logger.py

This file contains the logger functionality for printing
to standard out and standard error in a standardized way.
"""

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
    log_symbols = {
        'info': '🐝',
        'success': '✅',
        'error': '🛑',
        'warning': '⚠',
        'cookie': '🍪'
    }

    sym = log_symbols.get(log_type)
    if sym is not None:
        print(f"[{log_symbols.get(log_type, '🐝')}] ", end="")
    print(f"{msg}", end=end)

###   end of file   ###
