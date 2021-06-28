import re
from collections import namedtuple


Token = namedtuple('Token', 'span word')

token_split_pat = re.compile(r'\S+')

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
