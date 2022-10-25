#!/usr/bin/env  python3

"""Makefiler installation script"""

import os
import sys

def     install(home, rc_path):
    """Installation function"""
    new_rc = []
    with open(rc_path, 'r') as rc_file:
        for line in rc_file:
            if 'alias mkf' not in line:
                new_rc.append(line)
        new_rc.append("alias mkf='~/Utils/py_makefiler/py_makefiler.py'\n")
    with open(rc_path, 'w') as rc_file:
        for line in new_rc:
            print(line, file=rc_file, end='')
    os.system(f'mkdir -p {home}/Utils/py_makefiler 2> /dev/null; \
            cp makefiler.py {home}/Utils/py_makefiler/makefiler.py 2> /dev/null')
    print("Installation suceed, please reload your shell.")

def     uninstall(home, rc_path):
    """Uninstallation function"""
    new_rc = None
    with open(rc_path, 'r') as rc_file:
        new_rc = [line for line in rc_file if 'alias mkf' not in line]
    with open(rc_path, 'w') as rc_file:
        for line in new_rc:
            print(line, file=rc_file, end='')
    os.system(f'rm -rf {home}/Utils/py_makefiler 2> /dev/null')
    print("Makefiler has been successfully uninstalled.")

if __name__ == '__main__':
    print("""Makefiler 2.0 Installer""")
    CHOICE = input("""  1 - Install\n  2 - Uninstall\n  > """)
    try:
        HOME = os.environ.get('HOME')
        RC_PATH = HOME + '/.' + os.environ.get('SHELL') \
                .split('/')[-1] + 'rc'
        if CHOICE == '1':
            install(HOME, RC_PATH)
        elif CHOICE == '2':
            uninstall(HOME, RC_PATH)
        else:
            raise IndexError
    except Exception:
        print("Error: Can't install Makefiler 2.0", file=sys.stderr)
