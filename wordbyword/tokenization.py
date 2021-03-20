import re
from collections import namedtuple


Token = namedtuple('Token', 'span span_lc word')

token_split_pat = re.compile(r'\S+')

def position_to_line_and_col(string, pos):
    '''
    Convert a position within the given string (between 0 and len(string))
    to an index tuple in the form of (line, column). If the character
    at the given position is a newline character, ValueError is raised.
    '''
    try:
        if string[pos] == '\n':
            raise ValueError('Character at position {} is a newline character.'.format(pos))
    except IndexError:
        pass

    until_pos = string[:pos]
    line = until_pos.count('\n') + 1

    text_line = until_pos[until_pos.rfind('\n') + 1:]
    column = len(text_line)

    return line, column

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
                span_lc=(position_to_line_and_col(text, mstart), position_to_line_and_col(text, mend)),
                word=match.group(0)
            )
        )

    return L
