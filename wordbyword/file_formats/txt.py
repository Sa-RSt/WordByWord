# -*- coding: utf-8 -*-

from . import FileReader, check_extension, File

class TXTFileReader(FileReader):
    '''File reader that deals with plain text (.txt) files.'''

    def __init__(self):
        pass

    def read(self, filename):
        if not check_extension(filename, '.txt'):
            return None
        with open(filename, 'r') as file:
            return File(text=file.read(), current_word=0, comments=[])
