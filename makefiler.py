#!/usr/bin/env  python3

"""Script that automates makefiles creation"""

import sys
import getopt

def     error(msg='', hlp=False, ret_val=0):
    """Display error and help if needed and exit with chosen return value"""

    title = 'Makefiler 2.0 by Florian Cadet'
    help_str = """  Usage:
        mkf [OPTS] SRCS
    Options:
        -o  Output name
        -c  Langage (C or CPP)
        -l  Libraries (as one string)
        -f  Compiler flags (as one string)
    Flags:
        -h  This help"""

    if len(msg) != 0:
        print(f'Error: {msg}', file=sys.stderr)
    elif hlp:
        print(title)
    if hlp:
        print(help_str)
    sys.exit(ret_val)

if __name__ == '__main__':
    DATA = """NAME	=	{-o}
SRCS	=	{srcs}
OBJS	=	$(SRCS:{-c[s_ext]}={-c[o_ext]})
CC	=	{-c[cc]}
CFLAGS	=	{-f}
{-l}
all	:	$(NAME)

$(NAME)	:	$(OBJS)
		$(CC) $(CFLAGS) $^ -o $@ $(LIBS)

%{-c[o_ext]}	:	%{-c[s_ext]}
		$(CC) $(CFLAGS) -c $< -o $@

clean	:
		$(RM) $(OBJS)

fclean	:	clean
		rm -rf $(NAME)

re	:	fclean all"""
    OPTS = 'o:c:f:l:h'
    LANGUAGES = {'c': {'cc': 'gcc', 's_ext': '.c', 'o_ext': '.o'}, \
            'cpp': {'cc': 'g++', 's_ext': '.cpp', 'o_ext': '.opp'}}
    VALUES = {'srcs': None, \
            '-o': 'a.out', \
            '-c': LANGUAGES['c'], \
            '-l': '', \
            '-f': '-Wall -Wall -Wextra'}

    try:
        OPTIONS = getopt.getopt(sys.argv[1:], OPTS)
        if len(OPTIONS[1]) == 0:
            error('Arguments needed', True, 1)
        if len({x for x, _ in OPTIONS[0]}) != len(OPTIONS[0]):
            error('Duplicated option', True, 2)
        for opt, par in OPTIONS[0]:
            if opt == '-h':
                error(hlp=True)
            elif opt == '-c':
                if par.lower() not in LANGUAGES.keys():
                    error('Unsupported langage')
                VALUES['-c'] = LANGUAGES[par.lower()]
            elif opt == '-l':
                VALUES['-l'] = 'LIBS	=	' + par + '\n'
            else:
                VALUES[opt] = par
        VALUES['srcs'] = ' \\\n\t\t'.join(OPTIONS[1])
    except getopt.GetoptError as err:
        error(str(err), True, 3)

    with open('Makefile', 'w') as file:
        print(DATA.format(**VALUES), file=file)
