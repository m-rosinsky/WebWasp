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
        'success': '\033[32m!\033[0m',
        'error': '\033[31mError\033[0m',
        'warning': '\033[33mWarn\033[0m',
        'cookie': '🍪',
    }

    sym = log_symbols.get(log_type)
    if sym is not None:
        print(f"[{log_symbols.get(log_type, '!')}] ", end="")
    print(f"{msg}", end=end)

###   end of file   ###
