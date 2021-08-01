# -*- coding: utf-8 -*-

from . import FileReader, check_extension, File
import json

class JWBWFileIO(FileReader):
    '''
    File reader and writer for JWBW (JSON Word by Word) files.
    A more flexible and easily extensible version of WBWR files, that can store
    the user's progress (current word), bookmarks and other future features.
    '''

    def __init__(self):
        pass

    def read(self, filename):
        if not check_extension(filename, '.jwbw'):
            return None
        
        with open(filename, 'rb') as file:
            md_raw = bytearray()
            byte = file.read(1)
            while byte != b'\0':
                md_raw.extend(byte)
                byte = file.read(1)
            
            json_md = json.loads(bytes(md_raw))
            return File(text=file.read().decode(), current_word=json_md['current_word'], comments=json_md['comments'])
    
    def write(self, filename, filedata):
        with open(filename, 'w') as file:
            json.dump({'current_word': filedata.current_word, 'comments': filedata.comments}, file)
            file.write('\0')
            file.write(filedata.text)
