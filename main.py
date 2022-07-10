# -*- coding: utf-8 -*-

import os
import atexit

from wordbyword.gui.app import App
from wordbyword.gui.window import create_main_window
from wordbyword.settings import Settings
from sys import argv


@atexit.register
def save_all_settings():
    Settings.save()


assets_path = os.path.join(os.path.dirname(__file__), 'assets')
wnd = create_main_window(assets_path)

try:
    filename = argv[1]
except IndexError:
    filename = None

app = App(wnd, wnd, assets_path, filename)
wnd.rowconfigure(1, weight=1)
wnd.columnconfigure(1, weight=1)
app.get_tk_widget().grid(row=1, column=1, sticky='nsew')
wnd.update()
wnd.mainloop()
