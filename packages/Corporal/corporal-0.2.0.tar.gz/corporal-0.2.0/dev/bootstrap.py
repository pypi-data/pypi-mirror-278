# -*- coding: utf-8; -*-
"""
Bootstrap development for Corporal
"""

import os
import subprocess
import sys


here = os.path.abspath(os.path.dirname(__file__))


def bootstrap():
    if not inside_virtualenv():
        return

    # install wheel
    subprocess.run(['pip', 'install', 'wheel'],
                   check=True)

    # install invoke, sphinx
    subprocess.run(['pip', 'install', 'invoke', 'Sphinx'],
                   check=True)

    # run bootstrap task
    os.chdir(here)
    try:
        if sys.platform == 'win32':
            completed = subprocess.run(['invoke', 'bootstrap'])
        else:
            completed = subprocess.run(['invoke', '--echo', 'bootstrap'])
    except KeyboardInterrupt:
        sys.exit(130)  # 128 + SIGINT
    else:
        sys.exit(completed.returncode)


def inside_virtualenv():
    if not (hasattr(sys, 'real_prefix') or
            (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)):
        print("")
        print("Not running inside a virtual environment!")
        print("")
        print("Please create and activate that first, e.g. like:")
        print("")
        if sys.platform == 'win32':
            print("    py -m venv C:\\envs\\corporal")
            print("    C:\\envs\\corporal\\Scripts\\activate.bat")
        else:
            print("    python -m venv /srv/envs/corporal")
            print("    source /srv/envs/corporal/bin/activate")
        print("")
        return False
    return True


if __name__ == '__main__':
    bootstrap()
