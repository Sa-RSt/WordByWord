from .window import create_main_window
from .display import Display
from .buttons import ButtonsComponent
from .filepicker import Filepicker
from .speedchooser import SpeedChooser
from .map import Map
from .progress import Progress
from . import UIComponent
from tkinter import Frame
from time import perf_counter
from ..file_formats.read_file import read_file
from ..tokenization import split_tokens
from math import copysign


DEFAULT_TEXT = 'The quick brown fox jumped over the lazy dog.'


class App(UIComponent):
    def __init__(self, tkparent):
        super(App, self).__init__()

        self.frame = Frame(tkparent)

        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(3, weight=1)

        self.filepicker = Filepicker(self.frame, self.get_file)
        self.filepicker.get_tk_widget().grid(row=0, column=0, sticky='nw')

        self.progress = Progress(self.frame, len(split_tokens(DEFAULT_TEXT)))
        self.progress.get_tk_widget().grid(row=0, column=1, sticky='nsew')

        self.speed_chooser = SpeedChooser(self.frame)
        self.speed_chooser.get_tk_widget().grid(row=0, column=2, sticky='ne')

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
    
    def token_change(self, position):
        self.position = position - 1  # Position will increase by 1 on update.
        self.update_display()
    
    def updateloop(self):
        start = perf_counter()

        if not self.buttons.paused:
            self.update_display()
        
        elapsed = perf_counter() - start
        self.frame.after(int((self.speed_chooser.interval - elapsed*1000) / abs(self.buttons.factor)), self.updateloop)

    def update_display(self):
        newpos = int(self.position + copysign(1, self.buttons.factor))
        if newpos < len(self.tokens) and newpos >= 0:
            self.position = newpos
            self.progress.current = self.position
            tok = self.tokens[self.position]
            self.display.content = tok.word
            self.map.current_token = tok
            self.progress.update(self.speed_chooser.interval)

    def get_file(self, filename):
        content = read_file(filename)        # TODO handle exceptions
        self.set_contents(content)
    
    def set_contents(self, contents):
        self.map.text = contents       # Map tokenizes the text automatically
        self.tokens = self.map.tokens  #
        self.progress.total = len(self.tokens)
        self.position = -1  # self.update_display increments the position, so it will be set to 0
                            # after the first update.
        self.buttons.paused = True
        self.update_display()

    def get_tk_widget(self):
        return self.frame

