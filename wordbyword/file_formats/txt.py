from . import FileReader, check_extension

class TXTFileReader(FileReader):
    '''File reader that deals with plain text (.txt) files.'''

    def __init__(self):
        pass

    def read(self, filename):
        if not check_extension(filename, '.txt'):
            return None
        with open(filename, 'r') as file:
            return file.read()
