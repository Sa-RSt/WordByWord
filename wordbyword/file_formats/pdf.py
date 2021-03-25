import os

import pdfminer.high_level
from pdfminer.pdftypes import PSException

from . import FileReader

import inspect

class PDFFileReader(FileReader):
    '''File reader that reads from PDF files.'''

    def __init__(self):
        pass

    def read(self, filename):
        _, ext = os.path.splitext(filename)
        if ext.lower() != '.pdf':
            return None

        return pdfminer.high_level.extract_text(filename)
