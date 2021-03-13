import os
from . import FileReader

class TXTFileReader(FileReader):
    '''File reader that deals with plain text (.txt) files.'''

    def __init__(self):
        pass

    def read(self, filename):
        _, ext = os.path.splitext(filename)
        if ext.lower() != '.txt':
            return None
        with open(filename, 'r') as file:
            return file.read()
