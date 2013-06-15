#---------------------------------------------------------------
# Project         : pxe
# File            : pxeparse.py
# Copyright       : (C) 2013 by eNovance
# Author          : Frederic Lepied
# Created On      : Sat Jun 15 22:25:48 2013
# Purpose         : 
#---------------------------------------------------------------

import re

_TWO_LINES_REGEXP = re.compile('\n\s\n')
_SPACE_REGEXP = re.compile('\s*')

def parse(pxe_entry):
    res = {}
    for section in _TWO_LINES_REGEXP.split(pxe_entry):
        title = None
        for line in section.split('\n'):
            try:
                key, value = line.split(' ', 1)
            except ValueError:
                if _SPACE_REGEXP.search(line):
                    continue
                raise
            if not title:
                if key in ('DEFAULT', 'prompt', 'timeout'):
                    res[key] = value
                elif key == 'LABEL':
                    title = value
                    res[title] = {}
            else:
                res[title][key] = value
    return res

# pxeparse.py ends here
