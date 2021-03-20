from . import UIComponent
from tkinter.ttk import Label, Style
from tkinter import StringVar, Frame

class Display(UIComponent):
    '''
    UI component that displays the tokens.
    '''

    def __init__(self, tkparent):
        super(Display, self).__init__()

        self._content = ''
        self._contentvar = StringVar()
        self.frame = Frame(tkparent, background='gray')
        self.frame.columnconfigure(0, weight=1)
        self._iframe = Frame(self.frame, background='white')
        self._iframe.grid(row=0, column=0, padx=2, pady=2, sticky='nsew')
        style = Style(self.frame)
        style.configure('Display.TLabel', background='white', foreground='black')
        self._lbl = Label(self._iframe, textvariable=self._contentvar, style='Display.TLabel', font=('', 48), width=20)
        self._lbl.pack(anchor='center')

    @property
    def content(self):
        return self._content
    
    @content.setter
    def content(self, val):
        self._content = val
        self._contentvar.set(val)

    def get_tk_widget(self):
        return self.frame
