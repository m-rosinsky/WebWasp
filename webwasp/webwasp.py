"""
file: webwasp.py

This file contains the entry point of the console suite.
"""

import pkgutil

from webwasp.dispatch import Dispatcher

def main():
    """
    The entry point of the program.
    """

    __version__ = (pkgutil.get_data(__package__, "VERSION") or b"").decode("ascii").strip()

    banner = r"""
 __        __   _      __        __              
 \ \      / /__| |__   \ \      / /_ _ ___ _ __  
  \ \ /\ / / _ \ '_ \   \ \ /\ / / _` / __| '_ \ 
   \ V  V /  __/ |_) |   \ V  V / (_| \__ \ |_) |
    \_/\_/ \___|_.__/     \_/\_/ \__,_|___/ .__/ 
      Get Stinging                        |_|
                              Author: Mike Rosinsky 
    """
    print(banner)

    print(f"[🐝] Running WebWasp version {__version__}...")

    d = Dispatcher()
    d.run()

if __name__=='__main__':
    main()

###   end of file   ###
