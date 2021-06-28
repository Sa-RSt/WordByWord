from math import copysign
from re import compile
from time import perf_counter
from tkinter import Frame
from tkinter.filedialog import asksaveasfilename
from tkinter.messagebox import showerror, askyesnocancel

from ..file_formats import check_extension
from ..file_formats.read_file import read_file
from ..file_formats.wbwr import WBWRFile
from ..tokenization import split_tokens
from . import UIComponent
from .buttons import ButtonsComponent
from .display import Display
from .filepicker import Filepicker
from .map import Map
from .message_dialog import MessageDialog
from .progress import Progress
from .speedchooser import SpeedChooser
from .window import create_main_window

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
    def __init__(self, tkparent, root_window):
        super(App, self).__init__()

        self._interval_multiplier = 1

        self.root_window = root_window
        self.frame = Frame(tkparent)

        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(3, weight=1)

        self.overflow_frame = Frame(self.frame)

        self.progress = Progress(self.frame, len(split_tokens(DEFAULT_TEXT)))
        self.progress.get_tk_widget().grid(row=0, column=1, sticky='n')
        self.progress.on('save-progress', self.save_progress)

        self.speed_chooser = SpeedChooser(self.frame)
        self.speed_chooser.get_tk_widget().grid(row=0, column=2, sticky='ne')

        self.filepicker = Filepicker(self.frame)
        self.filepicker.get_tk_widget().grid(row=0, column=0, sticky='nw')
        self.filepicker.on('file-change', self.get_file)

        self.display = Display(self.frame)
        self.display.get_tk_widget().grid(row=1, column=0, columnspan=3)

        self.buttons = ButtonsComponent(self.frame)
        self.buttons.get_tk_widget().grid(row=2, column=0, columnspan=3)

        self.map = Map(self.frame)
        self.map.on('token-change', self.token_change)
        self.map.get_tk_widget().grid(row=3, column=0, columnspan=3)

        self.frame.after(self.speed_chooser.interval, self.updateloop)

        self.set_contents(DEFAULT_TEXT)
        self.position = 0

        self.root_window.protocol('WM_DELETE_WINDOW', self.on_quit_button)
    
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

    def get_file(self, filename):
        if not filename:
            return
        mbox = MessageDialog(self.get_tk_widget(), 'Word by Word Reader: Loading...', 'Loading. Please wait...')
        try:
            try:
                content = read_file(filename)
            except Exception as exc:
                self.filepicker.filename = ''
                showerror('Word by Word Reader - Error', 'We are sorry for the inconvenience. Could not read file. Error details: ' + str(exc))
                return
            if content is not None:
                if isinstance(content, str):
                    self.set_contents(content)
                elif isinstance(content, WBWRFile):
                    self.set_contents(content.text)
                    self.position = content.current_word
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
        if check_extension(fname, '.wbwr'):
            self.create_wbwr(fname)
            self.progress.trigger('progress-saved')
        else:
            output = asksaveasfilename(filetypes=[('Word by Word Reader progress files', '.wbwr')], defaultextension='.wbwr')
            if output:
                self.create_wbwr(output)
                self.filepicker.filename = output
                self.save_progress()

    def create_wbwr(self, fname):
        f = WBWRFile(fname)
        f.current_word = max(self.position - 1, 0)  # Position will be incremented on each update
        f.text = self.map.text
        return f

    def on_quit_button(self):
        fname = self.filepicker.filename

        if not fname.strip():
            self.root_window.destroy()
            return None

        if not check_extension(fname, '.wbwr'):
            self.save_or_confirm_quit()
            return None
        
        f = WBWRFile(self.filepicker.filename)
        if f.current_word != self.position - 1:
            self.save_or_confirm_quit()
            return None
        
        self.root_window.destroy()

    def save_or_confirm_quit(self):
        ans = askyesnocancel('Save Progress - Word by Word reader', 'Would you like to save your progress, so you can resume reading later?')
        if ans is True:
            self.save_progress()
            self.root_window.destroy()
        elif ans is False:
            self.root_window.destroy()

    def get_tk_widget(self):
        return self.frame

