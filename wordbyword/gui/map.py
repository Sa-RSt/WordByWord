from . import UIComponent
from tkinter import Frame
from tkinter.ttk import Button
from tkinter.scrolledtext import ScrolledText

def _tk_index(idx):
    '''
    Convert a (line, column) tuple into a
    tkinter-suitable 'line.column' string.
    '''
    return '{}.{}'.format(idx[0], idx[1])


class Map(UIComponent):
    def __init__(self, tkparent):
        self._current_token = None
        self.frame = Frame(tkparent)

        self.textw = ScrolledText(self.frame, state='disabled')
        self.textw.tag_configure('currentToken', underline=True)
        self.textw.grid(row=0, column=0, sticky='nsew')

        self.btn_scroll_to_current = Button(self.frame, text='Go to current word', command=self.on_scroll_to_current)
        self.btn_scroll_to_current.grid(row=1, column=0)

        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

    @property
    def current_token(self):
        return self._current_token

    @current_token.setter
    def current_token(self, val):
        self._current_token = val
        self.textw.tag_remove('currentToken', '1.0', 'end')

        if self._current_token is not None:
            self.textw.tag_add('currentToken', *self._current_token_tk_span())

    @property
    def text(self):
        return self.textw.get('1.0', 'end')
    
    @text.setter
    def text(self, val):
        self.current_token = None
        self.textw.config(state='normal')  # Can't edit text in disabled mode
        self.textw.delete('1.0', 'end')
        self.textw.insert('1.0', val)
        self.textw.config(state='disabled')

    def get_tk_widget(self):
        return self.frame

    def on_scroll_to_current(self):
        self.textw.see(self._current_token_tk_span()[0])

    def _current_token_tk_span(self):
        '''
        Return current token span as a 2-tuple
        in the form (start index, end index). The indices
        are suitable for use in tkinter.
        '''
        return _tk_index(self._current_token.span_lc[0]), _tk_index(self._current_token.span_lc[1])
