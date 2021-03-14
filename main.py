from wordbyword.gui.app import App
from wordbyword.gui.window import create_main_window

wnd = create_main_window()
app = App(wnd)
wnd.rowconfigure(1, weight=1)
wnd.columnconfigure(1, weight=1)
app.get_tk_widget().grid(row=1, column=1, sticky='nsew')
wnd.update()
wnd.minsize(wnd.winfo_width(), wnd.winfo_height())
wnd.mainloop()
