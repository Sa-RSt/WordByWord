# -*- coding: utf-8 -*-

import re
from collections import namedtuple


Token = namedtuple('Token', 'span word')

# Dash codes source: https://jkorpela.fi/dashes.html
# Dashes cannot break words at the end of a line. Hyphens can.
_DASHES = '\u2011\u2012\u2013\u2014\u2015\u2212\u2e3a\u2e3b\u301c\u3030\u2053\u30a0\ufe31\ufe32\ufe58'
token_split_pat = re.compile(r'[{D}]*[^\s{D}]+[{D}]*{N}?'.format(D=_DASHES, N='\n'))

def split_tokens(text):
    '''
    Split the text into tokens.
    A token is defined as a word plus all of its
    adjacent punctuation characters.
    Returns a list of tuples of
    (token start and end, token start and end in lines and columns, token text)
    '''
    L = []
    for match in token_split_pat.finditer(text):
        mstart = match.start()
        mend = match.end()
        L.append(
            Token(
                span=(mstart, mend),
                word=match.group(0)
            )
        )

    return L
