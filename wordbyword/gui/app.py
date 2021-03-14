from .window import create_main_window
from .display import Display
from .buttons import ButtonsComponent
from .filepicker import Filepicker
from . import UIComponent
from tkinter import Frame
from time import perf_counter
from ..file_formats.read_file import read_file
from ..tokenization import split_tokens


class App(UIComponent):
    def __init__(self, tkparent):
        self.frame = Frame(tkparent)

        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(1, weight=1)

        self.filepicker = Filepicker(self.frame, self.get_file)
        self.filepicker.get_tk_widget().grid(row=0, column=1)

        self.display = Display(self.frame)
        self.display.get_tk_widget().grid(row=1, column=1)

        self.buttons = ButtonsComponent(self.frame)
        self.buttons.get_tk_widget().grid(row=2, column=1)

        self.interval = 500

        self.frame.after(self.interval, self.updateloop)

        self.tokens = 'The quick brown fox jumps over the lazy dog.'.split()
        self.position = 0
    
    def updateloop(self):
        start = perf_counter()

        if not self.buttons.paused:
            self.update_display()
        
        elapsed = perf_counter() - start
        self.frame.after(self.interval - int(elapsed*1000), self.updateloop)

    def update_display(self):
        if self.position < len(self.tokens):
            self.display.content = self.tokens[self.position]
            self.position += 1

    def get_file(self, filename):
        self.tokens = ['']
        self.tokens = split_tokens(read_file(filename))  # TODO handle exceptions
        self.position = 0
        self.buttons.paused = True
        self.update_display()

    def get_tk_widget(self):
        return self.frame

