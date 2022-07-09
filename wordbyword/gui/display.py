# -*- coding: utf-8 -*-

from wordbyword.internationalization import getTranslationKey
from . import UIComponent
from tkinter.ttk import Label, Style
from tkinter import StringVar, Frame
from . import colors
from ..file_formats import IMAGE_ANNO

class Display(UIComponent):
    '''
    UI component that displays the tokens.
    '''

    def __init__(self, tkparent):
        super(Display, self).__init__()

        self._content = ''
        self._lang = 'en'
        self._contentvar = StringVar()
        self.frame = Frame(tkparent, background='gray')
        self.frame.columnconfigure(0, weight=1)
        self._iframe = Frame(self.frame, background='white')
        self._iframe.grid(row=0, column=0, padx=2, pady=2, sticky='nsew')
        self.style = Style(self.frame)
        self._lbl = Label(self._iframe, textvariable=self._contentvar, style='Display.TLabel', font=('', 30), width=50, anchor='center')
        self._lbl.pack(anchor='center')

        self.on('update-state', self.update_state)

    @property
    def content(self):
        return self._content
    
    @content.setter
    def content(self, val):
        self._content = val
        vals = val.strip()
        if vals == IMAGE_ANNO:
            self._contentvar.set(getTranslationKey(self._lang, 'image.redirect'))
        else:
            self._contentvar.set(vals)

    def update_state(self, state):
        self._iframe.config(bg=colors.DISPLAY[state.theme])
        self.style.configure('Display.TLabel', background=colors.DISPLAY[state.theme], foreground=colors.TEXT[state.theme])
        self._lang = state.language
        if self._content.strip() == IMAGE_ANNO:
            self._contentvar.set(getTranslationKey(self._lang, 'image.redirect'))

    def get_tk_widget(self):
        return self.frame
