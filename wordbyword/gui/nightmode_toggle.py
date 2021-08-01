# -*- coding: utf-8 -*-

from . import UIComponent
from tkinter import Button
from . import colors
from ..internationalization import getTranslationKey

class NightmodeToggle(UIComponent):
    def __init__(self, tkparent):
        super(NightmodeToggle, self).__init__()
        self._enabled = False
        self._lang = 'en'
        self.btn = Button(tkparent, command=self.toggle, text='Light theme')

        self.on('update-state', self.update_state)
    
    @property
    def enabled(self):
        return self._enabled
    
    @enabled.setter
    def enabled(self, val):
        self._enabled = val
        if val:
            self.trigger('nightmode-state', 1)
            self._update_button_text()
        else:
            self.trigger('nightmode-state', 0)
            self._update_button_text()
        self.btn.config(bg=colors.BUTTON[val], fg=colors.TEXT[val])

    def update_state(self, state):
        self._lang = state.language
        self._update_button_text()

    def _update_button_text(self):
        if self._enabled:
            self.btn.config(text=getTranslationKey(self._lang, 'themeToggle.lightTheme'))
        else:
            self.btn.config(text=getTranslationKey(self._lang, 'themeToggle.darkTheme'))

    def toggle(self):
        self.enabled = not self.enabled

    def get_tk_widget(self):
        return self.btn
