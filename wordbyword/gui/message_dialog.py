# -*- coding: utf-8 -*-

from tkinter import Toplevel
from tkinter import Label
from tkinter.simpledialog import Dialog

class MessageDialog(Toplevel):
    def __init__(self, parent, title, message):
        Toplevel.__init__(self, parent)
        self.title(title)
        Label(self, text=message).pack(padx=20, pady=20)
        self.resizable(False, False)
        self.wait_visibility()
        self.grab_set()
        self.update()
        self.update_idletasks()
