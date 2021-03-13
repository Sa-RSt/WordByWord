from .txt import TXTFileReader

reader_order = [
    TXTFileReader()
]

def read_file(filename):
    '''
    Try to read the file with every FileReader, in the order
    specified by the 'reader_order' list. Returns the text result
    of the first FileReader that succeeds. If the file format is not
    recognized by any of the readers, return None.
    '''
    for fr in reader_order:
        text = fr.read(filename)
        if text is not None:
            return text
    return None
