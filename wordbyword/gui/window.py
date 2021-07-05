import tkinter as tk

def create_main_window(iconpath):
    wnd = tk.Tk()
    wnd.iconphoto(True, tk.PhotoImage(file=iconpath))
    wnd.title('Word by Word Reader')
    return wnd
