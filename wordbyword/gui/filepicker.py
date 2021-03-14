from . import UIComponent
from tkinter.filedialog import askopenfilename
from tkinter import Frame
from tkinter.ttk import Button, Label


class Filepicker(UIComponent):
    def __init__(self, tkparent, onchange):
        '''
        @param onchange: callable object that will be called when the
        selected filename changes.
        '''

        self.onchange = onchange

        self.frame = Frame(tkparent)

        self.btn_pick = Button(self.frame, text='Pick a file...', command=self.onpick)
        self.btn_pick.grid(row=0, column=0)

        self.filename_entry = Label(self.frame)
        self.filename_entry.grid(row=0, column=1)
        self.frame.columnconfigure(1, weight=1)
    
    def get_tk_widget(self):
        return self.frame
    
    def onpick(self):
        filename = askopenfilename(filetypes=[('Text files', '.txt')])
        if filename:
            self.filename_entry.config(text=filename)
            self.onchange(filename)
