from abc import ABC, abstractmethod
import os

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
        Try to read a file and return its text.
        Returns None if the file format is not supported by
        this FileReader.
        '''

        return NotImplemented
