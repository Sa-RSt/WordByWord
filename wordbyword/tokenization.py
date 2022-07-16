# -*- coding: utf-8 -*-

import re
from collections import namedtuple


Token = namedtuple('Token', 'span word')

# TODO: Maybe mend hyphen-separated words

# Hyphen codes source: https://jkorpela.fi/dashes.html
hyphens = '\u058a\u05be\u2010\u2011\u2012\u2013\u2014\u2015\u2053\u207b\u208b\u2212\u2e17\u2e3a\u2e3b\u301c\u3030\u30a0\ufe31\ufe32\ufe58\ufe63\uff0d|-'
token_split_pat = re.compile(r'[{H}]*[^\s{H}]+[{H}]*{N}?'.format(H=hyphens, N='\n'))

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
