#!/usr/bin/env python3
import os
import sys
import subprocess
import tempfile


default_prompt = ''.join([
    r'\[\e]0;\u@\h: \w\a\]',
    r'${debian_chroot:+($debian_chroot)}',
    # Reset/normal, bold, green foreground
    r'\[\033[01;32m\]',
    r'\u@\h',
    # Reset/normal
    r'\[\033[00m\]',
    r':',
    # Reset/normal, bold, blue foreground
    r'\[\033[01;34m\]',
    r'\w',
    # Reset/normal
    r'\[\033[00m\]',
    r'\$ '
])


NONPRINT_START = r'\['
NONPRINT_END = r'\]'
CSI = r'\033['


def csi(*contents):
    return CSI + ''.join(contents)

def nonprint(*contents):
    return ''.join([NONPRINT_START, ''.join(contents), NONPRINT_END])


CSI_RESET_BOLD_RED_FG = csi('01;31m')
CSI_RESET_BOLD_GREEN_FG = csi('01;32m')
CSI_RESET_BOLD_BLUE_FG = csi('01;34m')
CSI_RESET = csi('00m')

NPCSI_RESET_BOLD_RED_FG = nonprint(CSI_RESET_BOLD_RED_FG)
NPCSI_RESET_BOLD_GREEN_FG = nonprint(CSI_RESET_BOLD_GREEN_FG)
NPCSI_RESET_BOLD_BLUE_FG = nonprint(CSI_RESET_BOLD_BLUE_FG)
NPCSI_RESET = nonprint(CSI_RESET)


ESCAPE_TIME_24 = r'\t'
ESCAPE_USERNAME = r'\u'
ESCAPE_HOSTNAME_SHORT = r'\h'
ESCAPE_CWD_HOMEABBR = r'\w'
ESCAPE_NEWLINE = r'\n'
ESCAPE_DOLLAR_OR_HASH = r'\\$'


ps1_contents = ''.join([
    # Nonprintable: set the window name for xterm
    nonprint(
        # Sends an "os command" to the xterm to set the window name.
        r'\e]0;',
        ESCAPE_USERNAME,
        '@',
        ESCAPE_HOSTNAME_SHORT,
        ': ',
        ESCAPE_CWD_HOMEABBR,
        # Ends the "os command"
        r'\a',
    ),

    # First line: user, host, time, cwd
    NPCSI_RESET,
    '[',
    NPCSI_RESET_BOLD_GREEN_FG,
    ESCAPE_USERNAME,
    NPCSI_RESET,
    '@',
    NPCSI_RESET_BOLD_GREEN_FG,
    ESCAPE_HOSTNAME_SHORT,
    NPCSI_RESET,
    '] ',
    ESCAPE_TIME_24,
    ' ',
    NPCSI_RESET_BOLD_BLUE_FG,
    ESCAPE_CWD_HOMEABBR,
    NPCSI_RESET,

    # Second (optional) line: git info
    r'\$(_git_info_line)',
    ESCAPE_NEWLINE,

    # Third line: prompt marker
    '--> ',
    ESCAPE_DOLLAR_OR_HASH,
    ' ',
    NPCSI_RESET,  # Just be sure it's all reset
])


git_info_line_function = \
r'''_git_info_line() {{
    BRANCH_NAME=$(
        git branch --list 2> /dev/null |
            sed -e '/^[^*]/d' -e 's/* \(.*\)/\1/'
    )
    if [ -n "$BRANCH_NAME" ]; then
        echo -e "\\ngit: branch={branch_name_varref}"
    fi
}};
'''.format(
    branch_name_varref=''.join([
        CSI_RESET_BOLD_RED_FG,
        '$BRANCH_NAME',
        CSI_RESET,
    ])
)
# TODO: Add the repo name (parent dir of .git or maybe two parents?)


def show_effects():
    _, bashinit = tempfile.mkstemp()
    try:
        bashinit_contents = '\n'.join([
            git_info_line_function,
            'export PS1="{0}"\n'.format(ps1_contents),
        ])
        print('Writing init to', bashinit)
        print('Contents:\n')
        print(bashinit_contents)
        with open(bashinit, 'w') as f:
            f.write('source ~/.bashrc\n')
            f.write(bashinit_contents)
            f.write('export PS1="TESTPROMPT $PS1"\n')
        subprocess.call(['/bin/bash', '--rcfile', bashinit, '-i'])
    finally:
        os.remove(bashinit)


def main():
    _, arg = sys.argv
    if arg == 'demo':
        show_effects()
    else:
        print('unknown arg "{0}"'.format(arg))
        sys.exit(1)

if __name__ == '__main__':
    main()
