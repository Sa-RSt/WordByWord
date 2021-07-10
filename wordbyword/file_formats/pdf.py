import pdfminer.high_level
from pdfminer.pdftypes import PSException
from string import whitespace

from . import FileReader, check_extension

class PDFFileReader(FileReader):
    '''File reader that reads from PDF files.'''

    def __init__(self):
        pass

    def read(self, filename):
        if not check_extension(filename, '.pdf'):
            return None

        raw = pdfminer.high_level.extract_text(filename)
        for char in whitespace:
            while char + char in raw:
                raw = raw.replace(char + char, char)
        return raw
