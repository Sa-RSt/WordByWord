import os
from tkinter import Frame
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Button, Label

from . import UIComponent


LABEL_WIDTH = 50


def _file_shorten(path, n):
    '''
    Shortens a file path to display it to the user,
    so that it contains a maximum of n characters.
    '''
    filename = os.path.basename(path)
    if len(filename) <= n:
        return filename
    name, ext = os.path.splitext(filename)
    reserved = 2+len(ext)
    if reserved >= n:
        return '........'
    namestop = n - reserved
    name_trunc = name[:namestop]
    return name_trunc + '..' + ext

class Filepicker(UIComponent):
    def __init__(self, tkparent):
        super(Filepicker, self).__init__()
        self._filename = ''

        self.frame = Frame(tkparent)

        self.btn_pick = Button(self.frame, text='Pick a file (.PDF or .TXT)...', command=self.onpick)
        self.btn_pick.grid(row=0, column=0)

        self.filename_entry = Label(self.frame, width=LABEL_WIDTH)
        self.filename_entry.grid(row=0, column=1)

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, val):
        self._filename = val
        display_text = _file_shorten(val, 30)
        self.filename_entry.config(
            text=display_text,
            width=50 - LABEL_WIDTH  # If the width is not fixed, the widget may vary in size whenever the text changes
        )
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
