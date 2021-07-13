from . import UIComponent
from tkinter import Button
from . import colors

class NightmodeToggle(UIComponent):
    def __init__(self, tkparent):
        super(NightmodeToggle, self).__init__()
        self._enabled = False
        self.btn = Button(tkparent, command=self.toggle, text='Light theme')
        self.toggle()
    
    @property
    def enabled(self):
        return self._enabled
    
    @enabled.setter
    def enabled(self, val):
        self._enabled = val
        if val:
            self.trigger('nightmode-state', True)
            self.btn.config(text='Light theme')
        else:
            self.trigger('nightmode-state', False)
            self.btn.config(text='Dark theme')
        self.btn.config(bg=colors.BUTTON[val], fg=colors.TEXT[val])

    def toggle(self):
        self.enabled = not self.enabled

    def get_tk_widget(self):
        return self.btn
