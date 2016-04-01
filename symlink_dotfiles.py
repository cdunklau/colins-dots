#!/usr/bin/env python
from __future__ import print_function
import sys
import os
import errno
import shutil


this_dir = os.path.dirname(os.path.abspath(__file__))
home_dir = os.path.expanduser('~')

dotfiles = ('.bashrc', '.vimrc', '.pythonrc', '.tmux.conf')

backup_suffix = '.bck'


def main():
    for dotfile in dotfiles:
        homedot = os.path.join(home_dir, dotfile)
        if nonlink(homedot):
            backup = homedot + backup_suffix
            print_stderr(
                'Backing up regular file {0} to {1}'.format(homedot, backup))
            shutil.copy(homedot, backup)
        target = os.path.join(this_dir, dotfile)
        link_name = os.path.join(home_dir, dotfile)
        print_stderr('Removing {0}'.format(link_name))
        try:
            os.remove(link_name)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise
        print_stderr(
            'Creating symbolic link {0} -> {1}'.format(link_name, target))
        os.symlink(target, link_name)


def nonlink(dotfile):
    return os.path.isfile(dotfile) and not os.path.islink(dotfile)


def print_stderr(*args):
    print(*args, file=sys.stderr)


if __name__ == '__main__':
    sys.exit(main())
