from tkinter import Menu, BooleanVar
from . import UIComponent
from ..internationalization import getTranslationKey

class ViewMenu(UIComponent):
    def __init__(self, tkparent, menu_entry):
        super(ViewMenu, self).__init__()
        self._lang = 'en'
        self.menu_entry = menu_entry
        self.menu = Menu(tkparent, tearoff=0)
        self.parent_menu = tkparent

        self.fullscreen = BooleanVar(False)
        self.focus = BooleanVar(False)

        self.menu.add_checkbutton(label=getTranslationKey(self._lang, 'view.fullscreen'), onvalue=1, offvalue=0, variable=self.fullscreen, command=self._on_change)
        self.menu.add_checkbutton(label=getTranslationKey(self._lang, 'view.focus'), onvalue=1, offvalue=0, variable=self.focus, command=self._on_change)

        self.on('update-state', self.update_state)
    
    def _on_change(self):
        self.trigger('view-mode', (self.fullscreen.get(), self.focus.get()))

    def update_state(self, state):
        self._lang = state.language
        self.parent_menu.entryconfig(self.menu_entry, label=getTranslationKey(self._lang, 'menu.view'))
        self.menu.entryconfig(0, label=getTranslationKey(self._lang, 'view.fullscreen'))
        self.menu.entryconfig(1, label=getTranslationKey(self._lang, 'view.focus'))

    def get_tk_widget(self):
        return self.menu
    
    def to_menu_cascade(self):
        return dict(label=getTranslationKey(self._lang, 'menu.view'), menu=self.menu)