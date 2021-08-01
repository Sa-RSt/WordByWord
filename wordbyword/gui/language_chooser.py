# -*- coding: utf-8 -*-

from tkinter import Menu
from . import UIComponent


class _lang:
    def __init__(self, code, languagechooser):
        self.languagechooser = languagechooser
        self.code = code

    def trigger(self, *_, **__):
        self.languagechooser.trigger('language', self.code)


class LanguageChooser(UIComponent):
    def __init__(self, tkparent, languages):
        super(LanguageChooser, self).__init__()
        self.menu = Menu(tkparent)
        for code, human_name in languages.items():
            self.menu.add_command(label=human_name, command=_lang(code, self).trigger)
    
    def get_tk_widget(self):
        return self.menu
