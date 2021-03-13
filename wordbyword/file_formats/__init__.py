from abc import ABC, abstractmethod

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
