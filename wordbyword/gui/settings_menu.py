# -*- coding: utf-8 -*-

from . import UIComponent
from ..internationalization import getTranslationKey
from tkinter import Menu

class SettingsMenu(UIComponent):
    def __init__(self, tkparent, menu_entry):
        super(SettingsMenu, self).__init__()
        self._lang = 'en'
        self.menu_entry = menu_entry
        self.menu = Menu(tkparent, tearoff=0)
        self.parent_menu = tkparent
        self.nightmode_toggle = NightmodeToggle(self.menu, 0)
        self.menu.add_command(self.nightmode_toggle.to_menu_entry())
        self.nightmode_toggle.on('nightmode-state', lambda x: self.trigger('nightmode-state', x))
        self.on('update-state', self.update_state)
    
    def update_state(self, state):
        self._lang = state.language
        self.parent_menu.entryconfig(self.menu_entry, label=getTranslationKey(self._lang, 'menu.settings'))
        self.nightmode_toggle.trigger('update-state', state)

    def get_tk_widget(self):
        return self.menu
    
    def to_menu_cascade(self):
        return dict(label=getTranslationKey(self._lang, 'menu.settings'), menu=self.menu)

class NightmodeToggle(UIComponent):
    def __init__(self, tkparent, menu_entry):
        super(NightmodeToggle, self).__init__()
        self._enabled = False
        self._lang = 'en'
        self.menu = tkparent
        self.menu_entry = menu_entry
        self.on('update-state', self.update_state)
    
    @property
    def enabled(self):
        return self._enabled
    
    @enabled.setter
    def enabled(self, val):
        self._enabled = val
        if val:
            self.trigger('nightmode-state', 1)
        else:
            self.trigger('nightmode-state', 0)

    def update_state(self, state):
        self._lang = state.language
        self.menu.entryconfigure(self.menu_entry, label=getTranslationKey(self._lang, 'themeToggle.changeTheme'))

    def toggle(self, *_, **__):
        self.enabled = not self.enabled

    def get_tk_widget(self):
        return NotImplemented
    
    def to_menu_entry(self):
        return dict(label=getTranslationKey(self._lang, 'themeToggle.changeTheme'), command=self.toggle)
