from . import UIComponent
from tkinter.filedialog import askopenfilename
from tkinter import Frame
from tkinter.ttk import Button, Label


class Filepicker(UIComponent):
    def __init__(self, tkparent):
        super(Filepicker, self).__init__()

        self.frame = Frame(tkparent)

        self.btn_pick = Button(self.frame, text='Pick a file...', command=self.onpick)
        self.btn_pick.grid(row=0, column=0)

        self.filename_entry = Label(self.frame)
        self.filename_entry.grid(row=0, column=1)
        self.frame.columnconfigure(1, weight=1)

    @property
    def filename(self):
        return self.filename_entry['text']

    @filename.setter
    def filename(self, val):
        self.filename_entry.config(text=val)
        self.trigger('file-change', val)

    def get_tk_widget(self):
        return self.frame
    
    def onpick(self):
        filename = askopenfilename(filetypes=[
            ('Files', '.txt; .pdf; .wbwr'),
            ('Text files', '.txt'),
            ('PDF files', '.pdf'),
            ('Word by Word Reader progress files', '.wbwr')
        ])
        if filename:
            self.filename = filename
