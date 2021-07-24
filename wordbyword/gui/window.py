import tkinter as tk
import os

def create_main_window(assets_path):
    wnd = tk.Tk()
    wnd.iconphoto(True, tk.PhotoImage(file=os.path.join(assets_path, 'icon.png')))
    wnd.title('Word by Word Reader')
    return wnd
