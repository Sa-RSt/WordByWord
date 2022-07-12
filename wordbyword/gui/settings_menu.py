# -*- coding: utf-8 -*-

from tkinter.font import families
from tkinter.ttk import Button, Label
from . import UIComponent
from ..internationalization import getTranslationKey
from tkinter import Frame, Listbox, Menu, Toplevel, BooleanVar
from itertools import chain

class SettingsMenu(UIComponent):
    def __init__(self, tkparent, menu_entry, pause_on_image):
        super(SettingsMenu, self).__init__()
        self._lang = 'en'
        self.menu_entry = menu_entry
        self.menu = Menu(tkparent, tearoff=0)
        self.parent_menu = tkparent

        self.nightmode_toggle = NightmodeToggle(self.menu, 0)
        self.menu.add_command(self.nightmode_toggle.to_menu_entry())
        self.nightmode_toggle.propagate_event_to('nightmode-state', self)
        self.propagate_event_to('update-state', self.nightmode_toggle)

        self.font_chooser = FontChooser(self.menu, 1)
        self.menu.add_command(self.font_chooser.to_menu_entry())
        self.font_chooser.propagate_event_to('font-changed', self)
        self.propagate_event_to('update-state', self.font_chooser)

        self.pause_on_image = PauseOnImage(self.menu, 2, pause_on_image)
        self.menu.add_checkbutton(self.pause_on_image.to_menu_entry())
        self.pause_on_image.propagate_event_to('pause-on-image-cfg', self)
        self.propagate_event_to('update-state', self.pause_on_image)

        self.on('update-state', self.update_state)
    
    def update_state(self, state):
        self._lang = state.language
        self.parent_menu.entryconfig(self.menu_entry, label=getTranslationKey(self._lang, 'menu.settings'))

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


class FontChooser(UIComponent):
    def __init__(self, tkparent, menu_entry):
        super(FontChooser, self).__init__()
        self._lang = 'en'
        self._font = 'serif'
        self.menu = tkparent
        self.menu_entry = menu_entry
        self.on('update-state', self.update_state)

    def pick_font(self):
        root = Toplevel(self.menu.master)
        picker_frame = Frame(root)
        
        Label(picker_frame, text=getTranslationKey(self._lang, 'fontChooser.label').format(self._font)).pack(anchor='n')
        
        picker = Listbox(picker_frame, selectmode='single', height=5)

        default_idx = 0
        font_map = dict()
        for idx, family in enumerate(chain(['serif'], sorted(families()))):
            picker.insert('end', family)
            font_map[idx] = family
            if family == self._font:
                default_idx = idx
        picker.selection_set(default_idx)
        picker.event_generate('<<ListboxSelect>>')

        picker.pack(expand=True, fill='both', anchor='s')

        picker_frame.grid(row=0, column=0, columnspan=2, sticky='nsew', padx=20, pady=20)

        def ok():
            font = font_map[picker.curselection()[0]]
            self._font = font
            print(self._font)
            self.trigger('font-changed', font)
            root.destroy()

        def cancel():
            root.destroy()

        Button(root, text=getTranslationKey(self._lang, 'ok'), command=ok).grid(row=1, column=0, padx=15, pady=15)
        Button(root, text=getTranslationKey(self._lang, 'cancel'), command=cancel).grid(row=1, column=1, padx=15, pady=15)

        root.title(getTranslationKey(self._lang, 'fontChooser.changeFont'))
        root.resizable(False, False)
        root.grab_set()
        

    def update_state(self, state):
        self._lang = state.language
        self._font = state.font
        self.menu.entryconfigure(self.menu_entry, label=getTranslationKey(self._lang, 'fontChooser.changeFont'))

    def get_tk_widget(self):
        return NotImplemented
    
    def to_menu_entry(self):
        return dict(label=getTranslationKey(self._lang, 'fontChooser.changeFont'), command=self.pick_font)

class PauseOnImage(UIComponent):
    def __init__(self, tkparent, menu_entry, pause_on_image):
        super(PauseOnImage, self).__init__()
        self.will_pause = BooleanVar(tkparent, pause_on_image)
        self._lang = 'en'
        self.menu = tkparent
        self.menu_entry = menu_entry
        self.on('update-state', self.update_state)

    def update_state(self, state):
        self._lang = state.language
        self.menu.entryconfigure(self.menu_entry, label=getTranslationKey(self._lang, 'pauseOnImage.checkbox'))

    def toggle(self):
        self.trigger('pause-on-image-cfg', self.will_pause.get())

    def get_tk_widget(self):
        return NotImplemented
    
    def to_menu_entry(self):
        return dict(label=getTranslationKey(self._lang, 'pauseOnImage.checkbox'), onvalue=1, offvalue=0, variable=self.will_pause, command=self.toggle)

