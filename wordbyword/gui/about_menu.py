# -*- coding: utf-8 -*-

from . import UIComponent
from ..internationalization import getTranslationKey
from tkinter import Menu
from tkinter.messagebox import showwarning, showinfo

class AboutMenu(UIComponent):
    def __init__(self, tkparent, menu_entry):
        super(AboutMenu, self).__init__()
        self._lang = 'en'
        self.menu_entry = menu_entry
        self.menu = Menu(tkparent, tearoff=0)
        self.parent_menu = tkparent

        self.menu.add_command(label=getTranslationKey(self._lang, 'about.menu'), command=self.show_about)
        self.menu.add_command(label=getTranslationKey(self._lang, 'healthAndSafety.buttonText'), command=self.show_health_and_safety_warning)

        self.on('update-state', self.update_state)
    
    def show_health_and_safety_warning(self):
        showwarning(getTranslationKey(self._lang, 'healthAndSafety.title'), getTranslationKey(self._lang, 'healthAndSafety.body'))

    def show_about(self):
        showinfo(getTranslationKey(self._lang, 'about.menu'), getTranslationKey(self._lang, 'about.body'))

    def update_state(self, state):
        self._lang = state.language
        self.parent_menu.entryconfig(self.menu_entry, label=getTranslationKey(self._lang, 'menu.about'))
        self.menu.entryconfig(0, label=getTranslationKey(self._lang, 'about.menu'))
        self.menu.entryconfig(1, label=getTranslationKey(self._lang, 'healthAndSafety.buttonText'))

    def get_tk_widget(self):
        return self.menu
    
    def to_menu_cascade(self):
        return dict(label=getTranslationKey(self._lang, 'menu.about'), menu=self.menu)
