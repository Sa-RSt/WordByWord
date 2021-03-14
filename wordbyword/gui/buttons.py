from . import UIComponent
from tkinter.ttk import Button
from tkinter import Frame


class ButtonsComponent(UIComponent):
    def __init__(self, tkparent):
        '''
        Initialize buttons.
        Arguments starting with on* must be callable objects
        to be called with no arguments when their respective
        buttons are pressed.
        '''
        self.frame = Frame(tkparent)
        self.btn_pause = Button(self.frame, text='Pause', command=self.onpause)
        self.btn_pause.grid(row=1,column=1,sticky='nsew')
        self._paused = False
    
    @property
    def paused(self):
        return self._paused
    
    @paused.setter
    def paused(self, val):
        self._paused = val
        if self.paused:
            self.btn_pause.config(text='Play')
        else:
            self.btn_pause.config(text='Pause')

    def get_tk_widget(self):
        return self.frame

    def onpause(self):
        self.paused = not self.paused
