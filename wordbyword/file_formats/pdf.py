import pdfminer.high_level
from pdfminer.pdftypes import PSException

from . import FileReader, check_extension

class PDFFileReader(FileReader):
    '''File reader that reads from PDF files.'''

    def __init__(self):
        pass

    def read(self, filename):
        if not check_extension(filename, '.pdf'):
            return None

        return pdfminer.high_level.extract_text(filename)
