# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
import os
from collections import namedtuple

IMAGE_ANNO = '<\u23a3\1IMG\1\u23a4>'

File = namedtuple('File', 'text current_word comments')

def check_extension(filename, ext):
    '''Convenience function to check if the given filename has the given extension.'''
    _, fext = os.path.splitext(filename)
    return fext.lower() == ext

class FileReader(ABC):
    '''
    Abstract base class for reading files with specific formats.
    '''

    @abstractmethod
    def read(self, filename):
        '''
        Try to read a file and return a File namedtuple.
        Returns None if the file format is not supported by
        this FileReader.
        '''

        return NotImplemented
