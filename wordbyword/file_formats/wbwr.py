from . import FileReader, check_extension
import struct


class WBWRFileReader(FileReader):
    '''
    File reader that reads from WBWR (Word by Word Reader) files.
    These files store text in a way that is easy to extract.
    They also save the current word.
    '''

    def __init__(self):
        pass

    def read(self, filename):
        if not check_extension(filename, '.wbwr'):
            return None
        
        return WBWRFile(filename)


FMT_CURRENT_WORD = '!i'

class WBWRFile:
    '''
    Class for reading and writing files in WBWR format.
    '''

    def __init__(self, filename):
        self.filename = filename
        try:
            self._init_existing()
        except FileNotFoundError:
            with open(self.filename, 'wb') as f:
                f.write(b'\0' * struct.calcsize(FMT_CURRENT_WORD))
            self._init_existing()

    def _init_existing(self):
        with open(self.filename, 'rb') as f:
            current_word_b = f.read(4)
            self._current_word = struct.unpack(FMT_CURRENT_WORD, current_word_b)[0]
            self._text = f.read().decode()
    
    def _write(self, text, word):
        with open(self.filename, 'wb') as f:
            f.write(struct.pack(FMT_CURRENT_WORD, word))
            f.write(text.encode())

    @property
    def current_word(self):
        return self._current_word
    
    @current_word.setter
    def current_word(self, index):
        self._current_word = index
        self._write(self.text, index)
    
    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, val):
        self._text = val
        self._write(val, self.current_word)
