import os
from tkinter import Frame
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Button, Label

from . import UIComponent


def _file_shorten(path, n):
    '''
    Shortens a file path for displaying to the user,
    so that it contains a maximum of n characters.
    '''
    filename = os.path.basename(path)
    if len(filename) <= n:
        return filename
    name, ext = os.path.splitext(filename)
    reserved = 2+len(ext)
    if reserved >= n:
        raise ValueError('Impossible to shorten filename: extension length + 2 is larger than n')
    namestop = n - reserved
    name_trunc = name[:namestop]
    return name_trunc + '..' + ext

class Filepicker(UIComponent):
    def __init__(self, tkparent):
        super(Filepicker, self).__init__()
        self._filename = ''

        self.frame = Frame(tkparent)

        self.btn_pick = Button(self.frame, text='Pick a file...', command=self.onpick)
        self.btn_pick.grid(row=0, column=0)

        self.filename_entry = Label(self.frame, width=50)
        self.filename_entry.grid(row=0, column=1)

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, val):
        self._filename = val
        self.filename_entry.config(text=_file_shorten(val, 30))
        self.trigger('file-change', val)

    def get_tk_widget(self):
        return self.frame
    
    def onpick(self):
        filename = askopenfilename(filetypes=[
            ('Files', '.txt; .pdf; .wbwr'),
            ('Text files', '.txt'),
            ('PDF files', '.pdf'),
            ('Word by Word Reader progress files', '.wbwr')
        ])
        if filename:
            self.filename = filename
