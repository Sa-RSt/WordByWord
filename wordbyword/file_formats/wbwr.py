# -*- coding: utf-8 -*-

from . import FileReader, check_extension, File
import struct

FMT_CURRENT_WORD = '!i'

class WBWRFileReader(FileReader):
    '''
    File reader that reads from legacy WBWR (Word by Word Reader) files.
    These files store text in a way that is easy to extract.
    They also save the current word.
    However, they don't store comments and bookmarks, because these features
    did not exist when this format was used.
    '''

    def __init__(self):
        pass

    def read(self, filename):
        if not check_extension(filename, '.wbwr'):
            return None
        with open(filename, 'rb') as f:
            current_word_b = f.read(4)
            current_word = struct.unpack(FMT_CURRENT_WORD, current_word_b)[0]
            text = f.read().decode()
        return File(text=text, current_word=current_word, comments=[])
