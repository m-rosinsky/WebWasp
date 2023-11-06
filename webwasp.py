"""
file: webwasp.py

This file contains the entry point of the console suite.
"""

import sys

try:
    import bs4
    import getch
    import requests
    import emoji
except ImportError:
    print("[🛑] Error: Missing Dependencies. ")
    print("[🛑] Run python3 -m pip install -r requirements.txt")
    sys.exit(1)

from src import console

def check_version():
    """
    This function validates the version of python being run.

    return -- True on valid version.
              False on invalid version.
    """
    required_version = (3, 7)

    return sys.version_info >= required_version

def main():
    """
    The entry point of the program.
    """

    # Validate version.
    if not check_version():
        sys.stderr.write("[🛑] Invalid version. WebWasp requires Python 3.7 or newer...\n")
        sys.exit(1)

    ww_version_major = 0
    ww_version_minor = 1
    ww_version_patch = "a"
    ww_version_string = f"{ww_version_major}.{ww_version_minor}{ww_version_patch}"

    banner = """
 __        __   _      __        __              
 \ \      / /__| |__   \ \      / /_ _ ___ _ __  
  \ \ /\ / / _ \ '_ \   \ \ /\ / / _` / __| '_ \ 
   \ V  V /  __/ |_) |   \ V  V / (_| \__ \ |_) |
    \_/\_/ \___|_.__/     \_/\_/ \__,_|___/ .__/ 
      Get Stinging                        |_|
                              Author: Mike Rosinsky 
    """
    print(banner)

    print(f"[🐝] Running WebWasp version {ww_version_string}...")

    con = console.Console()
    con.run()

if __name__=='__main__':
    main()

###   end of file   ###
