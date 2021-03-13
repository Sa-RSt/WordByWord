import re

token_split_pat = re.compile(r'\s+')

def split_tokens(text):
    '''
    Split the text into tokens.
    A token is defined as a word plus all of its
    adjacent punctuation characters.
    '''
    return token_split_pat.split(text)
