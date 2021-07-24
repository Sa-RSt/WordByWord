from . import UIComponent
from ..tokenization import split_tokens
from tkinter import Frame
from tkinter import Button
from tkinter.scrolledtext import ScrolledText
from tkinter.simpledialog import askstring, askinteger
from string import whitespace
from . import colors


def _findall(needle, haystack):
    '''
    Yield the indexes all occurences of the substring <needle>
    in the string <haystack>, from left to right
    '''
    accumulator = 0
    if not needle or not haystack:
        return
    idx = haystack.find(needle)
    while idx != -1:
        idx = haystack.find(needle)
        if idx == -1:
            return None
        yield idx + accumulator
        accumulator += idx + len(needle)
        haystack = haystack[idx+len(needle):]


def _tk_index(idx):
    '''
    Convert a single integer index to a tkinter index string.
    '''
    return '1.0 + {}c'.format(idx)

def _to_int_index(text, line, col):
    '''
    Convert a line and column index to a single integer index.
    '''
    current_line = 1
    for idx, char in enumerate(text):
        if current_line == line:
            return idx + col
        if char == '\n':
            current_line += 1
    raise ValueError('Invalid line', line)

class Map(UIComponent):
    def __init__(self, tkparent):
        super(Map, self).__init__()

        self._current_token = None
        self._tokens = []

        self.frame = Frame(tkparent)

        self.textw = ScrolledText(self.frame, state='disabled', cursor='plus')
        self.textw.bind('<Button-1>', self.on_click)
        self.textw.tag_configure('currentToken', underline=True)
        self.textw.grid(row=0, column=0, columnspan=3, sticky='nsew')

        self.btn_scroll_to_current = Button(self.frame, text='Go to current word', command=self.on_scroll_to_current)
        self.btn_scroll_to_current.grid(row=1, column=0, sticky='w')
        
        self.btn_find = Button(self.frame, text='Go to specific word (Find)...', command=self.on_find)
        self.btn_find.grid(row=1, column=1, sticky='e')

        self.btn_page = Button(self.frame, text='Jump to page...', command=self.on_go_to_page)
        self.btn_page.grid(row=1, column=2, sticky='e')

        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

        self.on('nightmode-state', self.update_nightmode_state)

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
    def tokens(self):
        return self._tokens

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
        self._tokens = split_tokens(val)

    def get_tk_widget(self):
        return self.frame

    def on_scroll_to_current(self):
        self.textw.see(self._current_token_tk_span()[0])

    def get_token_by_character_index(self, int_idx):
        for position, tok in enumerate(self.tokens):
            if int_idx in range(tok.span[0], tok.span[1]):
                return (tok, position)

    def on_find(self):
        try:
            occurences = None
            current = 0
            haystack = self.text.lower()
            old_needle = ''
            while 1:
                needle = askstring('Find | Word by Word Reader', 'Search or press ENTER to jump to next occurence:', initialvalue=old_needle).lower()
                self.textw.tag_remove('highlight', '1.0', 'end')
                if occurences is None or needle != old_needle:
                    current = 0
                    occurences = [x for x in _findall(needle, haystack)]
                if needle == old_needle:
                    current += 1
                start, end = _tk_index(occurences[current]), _tk_index(occurences[current] + len(needle))
                self.textw.tag_add('highlight', start, end)
                self.textw.tag_configure('highlight', background='red')
                self.textw.see(start)
                old_needle = needle
        finally:
            self.textw.tag_remove('highlight', '1.0', 'end')
    
    def on_go_to_page(self):
        text = self.text
        pagestarters = [0] + [x for x in _findall('\f', text)]
        pagecount = len(pagestarters)
        page = askinteger('Go to Page | Word by Word Reader', 'Number of pages: {}'.format(pagecount), minvalue=1, maxvalue=pagecount)
        if page:
            _idx = page - 1
            if _idx < 0:
                _idx = 0
            index = pagestarters[_idx]
            while text[index] in whitespace:
                index += 1
            tok, _ = self.get_token_by_character_index(index)
            start, end = _tk_index(tok.span[0]), _tk_index(tok.span[1])
            self.textw.tag_add('sel', start, end)
            self.textw.see(start)
            self.textw.focus_set()

    def on_click(self, evt):
        idx = self.textw.index('@{},{}'.format(evt.x, evt.y))
        line_s, col_s = idx.split('.')
        line = int(line_s)
        col = int(col_s)
        int_idx = _to_int_index(self.text, line, col)
        self.current_token, position = self.get_token_by_character_index(int_idx)
        self.trigger('token-change', position)
        

    def _current_token_tk_span(self):
        '''
        Return current token span as a 2-tuple
        in the form (start index, end index). The indices
        are suitable for use in tkinter.
        '''
        return _tk_index(self._current_token.span[0]), _tk_index(self._current_token.span[1])

    def update_nightmode_state(self, enabled):
        self.btn_find.config(bg=colors.BUTTON[enabled], fg=colors.TEXT[enabled])
        self.btn_page.config(bg=colors.BUTTON[enabled], fg=colors.TEXT[enabled])
        self.btn_scroll_to_current.config(bg=colors.BUTTON[enabled], fg=colors.TEXT[enabled])
        self.textw.config(bg=colors.DISPLAY[enabled], fg=colors.TEXT[enabled])
        self.frame.config(bg=colors.BACKGROUND[enabled])
