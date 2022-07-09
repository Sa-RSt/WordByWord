# -*- coding: utf-8 -*-

from pdfminer import high_level
from pdfminer import layout
import re

from . import FileReader, check_extension, File, IMAGE_ANNO


def _analyze_elements(out, elt):
    if isinstance(elt, layout.LTComponent):
        if isinstance(elt, layout.LTText):
            text = re.sub(r'\s', ' ', elt.get_text().replace('\0', ' ')).strip()
            while ' '*2 in text:
                text = text.replace('  ', ' ')
            out.append((elt.y0, text))
        elif isinstance(elt, layout.LTImage):
            out.append((elt.y0, IMAGE_ANNO))
        elif isinstance(elt, layout.LTContainer):
            for child in elt:
                _analyze_elements(out, child)


class PDFFileReader(FileReader):
    '''File reader that reads from PDF files.'''

    def __init__(self):
        pass

    def read(self, filename):
        if not check_extension(filename, '.pdf'):
            return None
    
        final_text = ''

        for page in high_level.extract_pages(filename):
            elements = []
            for elt in page:
               _analyze_elements(elements, elt)

            # Sort elements by their y-coordinate in descending order.
            # Essentially, this is the order in which the objects should be shown to the user.
            elements.sort(reverse=True)

            for _, text in elements:
                final_text += text
                final_text += '\n\n'
            final_text += '\f' # end page

        final_text = final_text[:-1] # remove trailing \f

        return File(text=final_text, current_word=0, comments=[])
