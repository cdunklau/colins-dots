#!/usr/bin/env python3
import os
import sys
import shlex
import subprocess
import tempfile
import time


class Namespace:
    pass

# These codes are the literal characters for PS1 as they would be written
# in a bash script. Example:
#   contents = 'export PS1="{0}@{1} {2} {3} "\n'.format(
#       CODE.USERNAME,
#       CODE.HOSTNAME_SHORT,
#       CODE.CWD_HOMEABBR,
#       CODE.DOLLAR_OR_HASH,
#   )
#   scriptfile.write(contents)
CODE = Namespace()
CODE.ESC = r'\033'
CODE.USERNAME = r'\u'
CODE.HOSTNAME_SHORT = r'\h'
CODE.CWD_HOMEABBR = r'\w'
CODE.NEWLINE = r'\n'
CODE.DOLLAR_OR_HASH = r'\\$'

CODE.NONPRINT_START = r'\['
CODE.NONPRINT_END = r'\]'

CODE.FMT_NONE = '$(tput sgr0)'
CODE.FMT_NONE_FORPROMPT = (
    CODE.NONPRINT_START + CODE.FMT_NONE + CODE.NONPRINT_END
)
CODE.FMT_DEFAULT_FOREGROUND = CODE.ESC + '[39m'
CODE.FMT_DEFAULT_FOREGROUND_FORPROMPT = (
    CODE.NONPRINT_START + CODE.FMT_DEFAULT_FOREGROUND + CODE.NONPRINT_END
)
CODE.FMT_DEFAULT_BACKGROUND = CODE.ESC + '[49m'
CODE.FMT_DEFAULT_BACKGROUND_FORPROMPT = (
    CODE.NONPRINT_START + CODE.FMT_DEFAULT_BACKGROUND + CODE.NONPRINT_END
)


COLOR = Namespace()
# Standard colors
COLOR.BLACK = 0
COLOR.RED = 1
COLOR.GREEN = 2
COLOR.YELLOW = 3
COLOR.BLUE = 4
COLOR.MAGENTA = 5
COLOR.CYAN = 6
COLOR.WHITE = 7
# High-intensity colors
COLOR.BLACK_HI = 8
COLOR.RED_HI = 9
COLOR.GREEN_HI = 10
COLOR.YELLOW_HI = 11
COLOR.BLUE_HI = 12
COLOR.MAGENTA_HI = 13
COLOR.CYAN_HI = 14
COLOR.WHITE_HI = 15


def color_start(colornum, bg=False, forprompt=False):
    if not 0 <= colornum <= 255:
        raise ValueError('color num must be between 0 and 255 (inclusive)')
    parts = [CODE.NONPRINT_START] if forprompt else []
    parts.extend([
        CODE.ESC,
        '[{fgbgcode};5;{colornum}m'.format(
            colornum=colornum,
            fgbgcode=48 if bg else 38,
        ),
    ])
    if forprompt:
        parts.append(CODE.NONPRINT_END)
    return ''.join(parts)


# TODO: Remove this
def colored(colornum, *contents, bg=False, forprompt=False):
    parts = [color_start(colornum, forprompt=forprompt, bg=bg)]
    parts.extend(contents)
    parts.append(CODE.FMT_NONE_FORPROMPT if forprompt else CODE.FMT_NONE)
    return ''.join(parts)


ps1_contents = ''.join([
    # First line: user, host, cwd
    color_start(COLOR.BLACK, forprompt=True),
    '[',
    color_start(COLOR.CYAN, forprompt=True),
    CODE.USERNAME,
    CODE.FMT_DEFAULT_FOREGROUND_FORPROMPT,
    '@',
    color_start(COLOR.BLUE_HI, forprompt=True),
    CODE.HOSTNAME_SHORT,
    color_start(COLOR.BLACK, forprompt=True),
    '] ',
    color_start(COLOR.GREEN, forprompt=True),
    CODE.CWD_HOMEABBR,
    CODE.FMT_DEFAULT_FOREGROUND_FORPROMPT,
    CODE.FMT_DEFAULT_BACKGROUND_FORPROMPT,
    # Second (optional) line: git info
    r'\$(_git_info_line)',
    CODE.NEWLINE,
    # Third line: prompt marker
    '--> ',
    CODE.DOLLAR_OR_HASH,
    ' ',
    CODE.FMT_NONE_FORPROMPT,  # Just be sure it's all reset
])


git_info_line_function = \
r'''_git_info_line() {{
    BRANCH_NAME=$(
        git branch --list 2> /dev/null |
            sed -e '/^[^*]/d' -e 's/* \(.*\)/\1/'
    )
    if [ -n "$BRANCH_NAME" ]; then
        echo -e "\\ngit: branch={branch_name_varref_colored}"
    fi
}};
'''.format(
    branch_name_varref_colored=colored(COLOR.RED, '$BRANCH_NAME'),
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


def test():
    echoargs = [
        ''.join([
            'should be normal ',
            color_start(COLOR.CYAN),
            'should be cyan',
            CODE.FMT_DEFAULT_FOREGROUND,
            ' should be normal',
        ]),
        ''.join([
            'should be normal ',
            color_start(COLOR.CYAN, bg=True),
            'should be cyan background',
            CODE.FMT_DEFAULT_BACKGROUND,
            ' should be normal',
        ]),
        ''.join([
            'should be normal ',
            color_start(COLOR.BLUE, bg=True),
            color_start(COLOR.YELLOW),
            'should be blue background, yellow foreground',
            CODE.FMT_DEFAULT_FOREGROUND,
            CODE.FMT_DEFAULT_BACKGROUND,
            ' should be normal',
        ]),
    ]
    for arg in echoargs:
        echo = ' '.join([
            '/bin/bash',
            '-c',
            """'echo -e "{0}"'""".format(arg),
        ])
        print('running', echo)
        subprocess.call(echo, shell=True)


def main():
    _, arg = sys.argv
    if arg == 'demo':
        show_effects()
    elif arg == 'test':
        test()
    else:
        print('unknown arg "{0}"'.format(arg))
        sys.exit(1)

if __name__ == '__main__':
    main()
