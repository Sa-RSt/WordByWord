# -*- coding: utf-8 -*-

from math import copysign
from re import compile
from time import perf_counter
from tkinter import Frame, Button, Menu
from tkinter.filedialog import asksaveasfilename
from tkinter.messagebox import showerror, askyesnocancel, showwarning

from ..file_formats import check_extension, File
from ..file_formats.jwbw import JWBWFileIO
from ..file_formats.wbwr import WBWRFileReader
from ..file_formats.read_file import read_file
from ..tokenization import split_tokens
from . import UIComponent
from .buttons import ButtonsComponent
from .display import Display
from .filepicker import Filepicker
from .map import Map
from .message_dialog import MessageDialog
from .progress import Progress
from .speedchooser import SpeedChooser
from .nightmode_toggle import NightmodeToggle
from .language_chooser import LanguageChooser
from . import colors
from ..settings import Settings
from ..internationalization import getTranslationKey, SUPPORTED_LANGUAGES
from .state import State

DEFAULT_TEXT = 'The quick brown fox jumped over the lazy dog.'
NON_WORD_START = compile(r'^\W')
NON_WORD_END = compile(r'\W$')

def has_punctuation(word):
    '''
    Check if the given word has any
    punctuation characters.
    '''
    return NON_WORD_END.search(word) or NON_WORD_START.search(word)

class App(UIComponent):
    def __init__(self, tkparent, root_window, assets_path, filename):
        super(App, self).__init__()

        self._interval_multiplier = 1
        self._state = State(theme=Settings['theme'], language=Settings['language'])

        self.root_window = root_window

        self.menu = Menu(root_window)

        self.language_chooser = LanguageChooser(self.menu, SUPPORTED_LANGUAGES)
        self.language_chooser.on('language', lambda language: self.update_state(State(theme=self._state.theme, language=language)))
        self.menu.add_cascade(label='Change Language/Mudar Idioma', menu=self.language_chooser.get_tk_widget())

        root_window.config(menu=self.menu)

        self.frame = Frame(tkparent)

        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(3, weight=1)

        self.progress = Progress(self.frame, len(split_tokens(DEFAULT_TEXT)))
        self.progress.get_tk_widget().grid(row=0, column=1, sticky='n')
        self.progress.on('save-progress', self.save_progress)

        self.speed_chooser = SpeedChooser(self.frame)
        self.speed_chooser.get_tk_widget().grid(row=0, column=2, sticky='ne')
        self.speed_chooser.speed = Settings['speed']
        self.speed_chooser.on('speed-change', self.on_speed_change)

        self.filepicker = Filepicker(self.frame)
        self.filepicker.get_tk_widget().grid(row=0, column=0, sticky='nw')
        self.filepicker.on('file-change', self.get_file)
        self.filepicker.on('will-pick-file', self.will_pick_file)

        self.display = Display(self.frame)
        self.display.get_tk_widget().grid(row=1, column=0, columnspan=3)

        self.buttons = ButtonsComponent(self.frame, assets_path)
        self.buttons.get_tk_widget().grid(row=2, column=0, columnspan=3)

        self.map = Map(self.frame)
        self.map.on('token-change', self.token_change)
        self.map.get_tk_widget().grid(row=3, column=0, columnspan=3)

        self.nightmode_toggle = NightmodeToggle(self.frame)
        self.nightmode_toggle.on('nightmode-state', lambda theme: self.update_state(State(theme=theme, language=self._state.language)))
        self.nightmode_toggle.get_tk_widget().grid(row=4, column=2)

        self.health_and_safety = Button(self.frame, text=getTranslationKey(self._state.language, 'healthAndSafety.buttonText'), command=self.show_health_and_safety_warning)
        self.health_and_safety.grid(row=4, column=1, pady=(20, 0))

        self.frame.after(self.speed_chooser.interval, self.updateloop)

        self.set_contents(DEFAULT_TEXT)
        self.position = 0

        self.root_window.protocol('WM_DELETE_WINDOW', self.on_quit_button)
        self.root_window.bind('<Control-f>', lambda _: self.map.on_find())
        self.root_window.bind('<Control-F>', lambda _: self.map.on_go_to_page())
        self.root_window.bind('<Control-v>', lambda _: self.map.on_scroll_to_current())

        if filename is not None:
            self.filepicker.filename = filename
        
        self.update_state(self._state)
        self.nightmode_toggle.enabled = Settings['theme']

        if not Settings['blink_warning_shown']:
            self.show_health_and_safety_warning()
            Settings['blink_warning_shown'] = True
            Settings.save()
    
    def token_change(self, position):
        self.position = position - 1  # Position will increase by 1 on update.
        self.update_display()
    
    def updateloop(self):
        start = perf_counter()

        if not self.buttons.paused:
            self._interval_multiplier = self.update_display()
        
        elapsed = perf_counter() - start
        self.frame.after(int(self._interval_multiplier * (self.speed_chooser.interval - elapsed*1000) / abs(self.buttons.factor)), self.updateloop)

    def update_display(self):
        newpos = int(self.position + copysign(1, self.buttons.factor))
        if newpos < len(self.tokens) and newpos >= 0:
            self.position = newpos
            self.progress.current = self.position
            tok = self.tokens[self.position]
            self.display.content = tok.word
            self.map.current_token = tok
            self.progress.update(self.speed_chooser.interval)

            if has_punctuation(tok.word):
                return 1.75
        return 1

    def will_pick_file(self):
        if not self.filepicker.filename:
            return
        ans = askyesnocancel(getTranslationKey(self._state.language, 'confirmSave.title'), getTranslationKey(self._state.language, 'confirmSave.body'))
        if ans is None:
            return True
        elif ans:
            self.save_progress()

    def get_file(self, filename):
        if not filename:
            return
        mbox = MessageDialog(self.get_tk_widget(), getTranslationKey(self._state.language, 'converting.title'), getTranslationKey(self._state.language, 'converting.body'))
        try:
            try:
                content = read_file(filename)
            except Exception as exc:
                self.filepicker.filename = ''
                showerror(
                    getTranslationKey(self._state.language, 'error.readFile.title'),
                    getTranslationKey(self._state.language, 'error.readFile.body').format(str(exc))
                )
                return
            if content is not None:
                self.set_contents(content.text)
                self.position = content.current_word
                self.map.comlist.load_comments(content.comments)
                self.update_display()
                
        finally:
            mbox.destroy()

    def set_contents(self, contents):
        self.map.text = contents       # Map tokenizes the text automatically
        self.tokens = self.map.tokens  #
        self.progress.total = len(self.tokens)
        self.position = -1  # self.update_display increments the position, so it will be set to 0
                            # after the first update.
        self.buttons.paused = True
        self.update_display()
    
    def save_progress(self):
        fname = self.filepicker.filename
        if check_extension(fname, '.jwbw'):
            self.create_jwbw(fname)
            self.progress.trigger('progress-saved')
        else:
            output = asksaveasfilename(filetypes=[(getTranslationKey(self._state.language, 'fileType.jwbw'), '.jwbw')], defaultextension='.jwbw')
            if output:
                self.create_jwbw(output)
                self.filepicker.filename = output
                self.save_progress()

    def create_jwbw(self, fname):
        cw = max(self.position - 1, 0)  # Position will be incremented on each update
        fio = JWBWFileIO()
        fio.write(fname, File(text=self.map.text, current_word=cw, comments=self.map.comlist.dump_comments()))

    def on_speed_change(self):
        self.progress.update(self.speed_chooser.interval)
        Settings['speed'] = self.speed_chooser.speed

    def on_quit_button(self):
        self.buttons.paused = True
        fname = self.filepicker.filename

        if not fname.strip():
            self.terminate_app()
            return None

        self.save_or_confirm_quit()    

    def save_or_confirm_quit(self):
        ans = askyesnocancel(getTranslationKey(self._state.language, 'confirmSave.title'), getTranslationKey(self._state.language, 'confirmSave.body'))
        if ans is True:
            self.save_progress()
            self.terminate_app()
        elif ans is False:
            self.terminate_app()
        
    def terminate_app(self):
        '''Exit the program.'''
        self.root_window.destroy()
        Settings.save()
        
    def update_state(self, state):
        self._state = state
        Settings['theme'] = state.theme
        Settings['language'] = state.language
        Settings.save()

        self.frame.config(bg=colors.BACKGROUND[state.theme])
        self.health_and_safety.config(bg=colors.BUTTON[state.theme], fg=colors.TEXT[state.theme], text=getTranslationKey(state.language, 'healthAndSafety.buttonText'))
        for comp in [self.progress, self.speed_chooser, self.filepicker, self.display, self.buttons, self.map, self.nightmode_toggle]:
            comp.trigger('update-state', state)

    def show_health_and_safety_warning(self):
        showwarning(getTranslationKey(self._state.language, 'healthAndSafety.title'), getTranslationKey(self._state.language, 'healthAndSafety.body'))

    def get_tk_widget(self):
        return self.frame

