# -*- coding: utf-8 -*-

from wordbyword.internationalization import getTranslationKey
from . import UIComponent
from tkinter.ttk import Label, Style
from tkinter import StringVar, Frame
from . import colors
from ..file_formats import IMAGE_ANNO

FONT_SIZE_DEFAULT = 30

WIDTH_DEFAULT = 1300
HEIGHT_DEFAULT = 50

WIDTH_FOCUS = 1500
HEIGHT_FOCUS = 300

class Display(UIComponent):
    '''
    UI component that displays the tokens.
    '''

    def __init__(self, tkparent):
        super(Display, self).__init__()

        self._content = ''
        self._lang = 'en'
        self._font = 'serif'
        self._focus = False
        self._focus_font_sz = 45
        self._contentvar = StringVar()
        self._special_contentvar = StringVar()

        self.frame = Frame(tkparent, background='gray')
        self.frame.columnconfigure(0, weight=1)
        self._iframe = Frame(self.frame, background='white', width=WIDTH_DEFAULT, height=HEIGHT_DEFAULT)
        self._iframe.grid(row=0, column=0, padx=2, pady=2, sticky='nsew')
        self.style = Style(self.frame)
        self._lbl = Label(self._iframe, textvariable=self._contentvar, style='Display.TLabel', font=(self._font, FONT_SIZE_DEFAULT), anchor='center')
        self._lbl.place(relx=0, rely=0, relheight=1, relwidth=1)
        self._special_lbl = Label(self._iframe, textvariable=self._special_contentvar, style='Display.TLabel', anchor='center')

        self._lbl.bind('<Double-Button-1>', lambda _: self.trigger('double-click'))
        self._special_lbl.bind('<Double-Button-1>', lambda _: self.trigger('double-click'))

        self.on('update-state', self.update_state)
        self.on('focus-mode', self.update_focus_mode)
        self.on('font-size-change', self.set_focus_mode_font_size)

    def _set_display(self, text, special):
        if special:
            self._contentvar.set('')
            self._special_contentvar.set(text)
            self._special_lbl.place(relx=0, rely=0, relheight=1, relwidth=1)
            self._lbl.place_forget()
        else:
            self._contentvar.set(text)
            self._special_contentvar.set('')
            self._lbl.place(relx=0, rely=0, relheight=1, relwidth=1)
            self._special_lbl.place_forget()

    def _set_font_size(self, sz):
        self._lbl.config(font=(self._font, sz))

    @property
    def content(self):
        return self._content
    
    @content.setter
    def content(self, val):
        self._content = val
        vals = val.strip()
        if vals == IMAGE_ANNO:
            self._set_display(getTranslationKey(self._lang, 'image.redirect'), True)
        else:
            self._set_display(vals, False)

    def update_state(self, state):
        self._iframe.config(bg=colors.DISPLAY[state.theme])
        self._lbl.configure(font=(state.font, FONT_SIZE_DEFAULT))
        self.style.configure('Display.TLabel', background=colors.DISPLAY[state.theme], foreground=colors.TEXT[state.theme])
        self._lang = state.language
        self._font = state.font
        if self._content.strip() == IMAGE_ANNO:
            self._contentvar.set(getTranslationKey(self._lang, 'image.redirect'))

    def update_focus_mode(self, focus):
        self._focus = focus
        if focus:
            self._iframe.config(width=WIDTH_FOCUS, height=HEIGHT_FOCUS)
            self._set_font_size(self._focus_font_sz)
        else:
            self._iframe.config(width=WIDTH_DEFAULT, height=HEIGHT_DEFAULT)
            self._set_font_size(FONT_SIZE_DEFAULT)

    def set_focus_mode_font_size(self, sz):
        self._focus_font_sz = sz
        if self._focus:
            self._set_font_size(sz)


    def get_tk_widget(self):
        return self.frame
