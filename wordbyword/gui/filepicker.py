import os
from tkinter import Frame, Button, Label
from tkinter.filedialog import askopenfilename

from . import UIComponent
from ..internationalization import getTranslationKey
from . import colors


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
        self._lang = 'en'

        self.frame = Frame(tkparent)

        self.btn_pick = Button(self.frame, text=getTranslationKey(self._lang, 'filePicker.pickAFile'), command=self.onpick)
        self.btn_pick.grid(row=0, column=0)

        self.filename_entry = Label(self.frame, width=LABEL_WIDTH)
        self.filename_entry.grid(row=0, column=1)

        self.on('update-state', self.update_state)

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
        if any(self.trigger('will-pick-file')):
            return
        filename = askopenfilename(filetypes=[
            (getTranslationKey(self._lang, 'fileType.*'), '.txt; .pdf; .wbwr; .jwbw'),
            (getTranslationKey(self._lang, 'fileType.txt'), '.txt'),
            (getTranslationKey(self._lang, 'fileType.pdf'), '.pdf'),
            (getTranslationKey(self._lang, 'fileType.wbwr'), '.wbwr'),
            (getTranslationKey(self._lang, 'fileType.jwbw'), '.jwbw'),
        ])
        if filename:
            self.filename = filename
    
    def update_state(self, state):
        self._lang = state.language
        self.frame.config(bg=colors.BACKGROUND[state.theme])
        self.btn_pick.config(bg=colors.BUTTON[state.theme], fg=colors.TEXT[state.theme], text=getTranslationKey(state.language, 'filePicker.pickAFile'))
        self.filename_entry.config(bg=colors.BACKGROUND[state.theme], fg=colors.TEXT[state.theme])
