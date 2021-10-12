# -*- coding: utf-8 -*-

from . import UIComponent
from .comments import CommentList
from ..tokenization import split_tokens
from ..internationalization import getTranslationKey
from tkinter import Frame, Button, Label, Toplevel, Entry, TclError
from tkinter.scrolledtext import ScrolledText
from tkinter.simpledialog import askinteger
from tkinter.messagebox import showinfo
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
        self._lang = 'en'

        self.frame = Frame(tkparent)

        self.mapframe = Frame(self.frame)

        self.textw = ScrolledText(self.mapframe, state='disabled', cursor='plus', width=100, selectforeground='blue')
        self.textw.bind('<ButtonRelease-1>', self.on_click)
        self.textw.grid(row=0, column=0, columnspan=4, sticky='nsew')

        self.btn_scroll_to_current = Button(self.mapframe, text=getTranslationKey(self._lang, 'map.toCurrentWord'), command=self.on_scroll_to_current)
        self.btn_scroll_to_current.grid(row=1, column=0, sticky='w')

        self.lbl_page = Label(self.mapframe, font=('', 16, 'bold'))
        self.lbl_page.grid(row=1, column=1, sticky='w', padx=40)
        
        self.btn_page = Button(self.mapframe, text=getTranslationKey(self._lang, 'map.goToPage.button'), command=self.on_go_to_page)
        self.btn_page.grid(row=1, column=2, sticky='e')

        self.btn_find = Button(self.mapframe, text=getTranslationKey(self._lang, 'map.find.button'), command=self.on_find)
        self.btn_find.grid(row=1, column=3, sticky='e')

        self.mapframe.grid(row=0, column=0)

        self.comlist = CommentList(self.frame)
        self.comlist.get_tk_widget().grid(row=0, column=1, sticky='nsew')
        self.comlist.on('highlight', self._highlight_comment_span)

        self.textw.bind('<Button-2>', lambda *_: self.comlist.on_add())
        self.textw.bind('<Button-3>', lambda *_: self.comlist.on_add())

        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

        self.on('update-state', self.update_state)

    @property
    def current_token(self):
        return self._current_token

    @current_token.setter
    def current_token(self, val):
        self._current_token = val
        self.textw.tag_remove('currentToken', '1.0', 'end')

        if self._current_token is not None:
            self.textw.tag_add('currentToken', *self._current_token_tk_span())
            self.lbl_page.configure(text=getTranslationKey(self._lang, 'map.currentPage').format(self.get_page_of_token(self._current_token), self.get_page_count()))

    @property
    def tokens(self):
        return self._tokens

    @property
    def text(self):
        return self.textw.get('1.0', 'end')
    
    @text.setter
    def text(self, val):
        try:
            del self._page_starters_cache
        except AttributeError:
            pass
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
        root = Toplevel(self.frame.master)
        root.title(getTranslationKey(self._lang, 'map.find.title'))
        frame = Frame(root)
        frame.pack()

        prev = Button(frame, text=getTranslationKey(self._lang, 'map.find.prev'))
        prev.grid(row=0, column=0)

        entry = Entry(frame)
        entry.grid(row=0, column=1)
        entry.focus()

        nxt = Button(frame, text=getTranslationKey(self._lang, 'map.find.next'))
        nxt.grid(row=0, column=2)

        occlbl = Label(frame)
        occlbl.grid(row=1, column=1)

        word = None
        occurrences = None
        current_idx = None

        def init_word(w):
            nonlocal word
            nonlocal occurrences
            nonlocal current_idx
            word = w
            occurrences = [(x, x + len(word)) for x in _findall(word, self.text.lower())]
            if occurrences:
                current_idx = 0
                update_ui()
            else:
                showinfo('Word by Word Reader', getTranslationKey(self._lang, 'map.find.nowords'))

        def update_ui():
            self.textw.tag_remove('hl_weak', '1.0', 'end')
            self.textw.tag_remove('hl_strong', '1.0', 'end')
            for idx, span in enumerate(occurrences):
                what_tag = 'hl_weak'
                if idx == current_idx:
                    what_tag = 'hl_strong'
                    self.textw.see(_tk_index(span[0]))
                
                if abs(idx - current_idx) <= 3:  # Only render near words for performance
                    self.textw.tag_add(what_tag, _tk_index(span[0]), _tk_index(span[1]))
            
            self.textw.tag_configure('hl_weak', background='gray')
            self.textw.tag_configure('hl_strong', background='red', foreground='white')

            occlbl.config(text=getTranslationKey(self._lang, 'map.find.occurrences').format(current_idx + 1, len(occurrences)))

        def on_prev():
            nonlocal current_idx

            w = entry.get().strip().lower()
            if not w:
                return

            if w != word:
                return init_word(w)
            
            if current_idx > 0:
                current_idx -= 1
                update_ui()
        
        def on_next():
            nonlocal current_idx
            
            w = entry.get().strip().lower()
            if not w:
                return

            if w != word:
                return init_word(w)
            
            if current_idx < len(occurrences)-1:
                current_idx += 1
                update_ui()
        
        def cleanup():
            self.textw.tag_remove('hl_weak', '1.0', 'end')
            self.textw.tag_remove('hl_strong', '1.0', 'end')
            root.destroy()
        
        prev.config(command=on_prev)
        nxt.config(command=on_next)
        entry.bind('<Return>', lambda *_: on_next())

        root.resizable(False, False)
        root.grab_set()
        root.protocol('WM_DELETE_WINDOW', cleanup)
    
    def get_page_starters(self):
        '''Return a list with the indices of the first characters of all pages.'''
        try:
            return self._page_starters_cache
        except AttributeError:
            self._page_starters_cache = [0] + [x for x in _findall('\f', self.text)]
            return self._page_starters_cache

    def get_page_count(self):
        return len(self.get_page_starters())

    def get_page_of_token(self, tok):
        count = 0
        index = tok.span[0]
        for pagestart in self.get_page_starters():
            if index >= pagestart:
                count += 1
            else:
                break
        return count

    def on_go_to_page(self):
        text = self.text
        pagestarters = self.get_page_starters()
        pagecount = self.get_page_count()
        page = askinteger(getTranslationKey(self._lang, 'map.goToPage.title'), getTranslationKey(self._lang, 'map.goToPage.body').format(self.get_page_of_token(self.current_token), pagecount), minvalue=1, maxvalue=pagecount)
        if page:
            _idx = page - 1
            if _idx < 0:
                _idx = 0
            index = pagestarters[_idx]
            try:
                while text[index] in whitespace:
                    index += 1
            except IndexError:  # This may happen if the last page(s) is/are blank
                while text[index - 1] in whitespace:
                    index -= 1
                index -= 1
            tok, _ = self.get_token_by_character_index(index)
            start, end = _tk_index(tok.span[0]), _tk_index(tok.span[1])
            self.textw.tag_add('sel', start, end)
            self.textw.see(start)
            self.textw.focus_set()

    def _highlight_comment_span(self, span):
        self.textw.tag_remove('comhl', '1.0', 'end')
        if span is not None:
            self.textw.tag_add('comhl', _tk_index(span[0]), _tk_index(span[1]))
            self.textw.tag_configure('comhl', background='green')
            self.textw.see(_tk_index(span[0]))

    def on_click(self, evt):
        try:
            self.textw.selection_get()
        except TclError:
            self.comlist.trigger('update-selection', None)

            idx = self.textw.index('@{},{}'.format(evt.x, evt.y))
            line_s, col_s = idx.split('.')
            line = int(line_s)
            col = int(col_s)
            int_idx = _to_int_index(self.text, line, col)
            self.current_token, position = self.get_token_by_character_index(int_idx)
            self.trigger('token-change', position)
        else:
            selfirst_line_s, selfirst_col_s = self.textw.index('sel.first').split('.')
            sellast_line_s, sellast_col_s = self.textw.index('sel.last').split('.')
            selfirst_line, selfirst_col, sellast_line, sellast_col = int(selfirst_line_s), int(selfirst_col_s), int(sellast_line_s), int(sellast_col_s)
            selfirst, sellast = _to_int_index(self.text, selfirst_line, selfirst_col), _to_int_index(self.text, sellast_line, sellast_col)
            self.comlist.trigger('update-selection', (selfirst, sellast))

    def _current_token_tk_span(self):
        '''
        Return current token span as a 2-tuple
        in the form (start index, end index). The indices
        are suitable for use in tkinter.
        '''
        return _tk_index(self._current_token.span[0]), _tk_index(self._current_token.span[1])

    def update_state(self, state):
        self._lang = state.language
        self.current_token = self.current_token  # Update page index

        self.btn_find.config(bg=colors.BUTTON[state.theme], fg=colors.TEXT[state.theme], text=getTranslationKey(state.language, 'map.find.button'))
        self.btn_page.config(bg=colors.BUTTON[state.theme], fg=colors.TEXT[state.theme], text=getTranslationKey(state.language, 'map.goToPage.button'))
        self.btn_scroll_to_current.config(bg=colors.BUTTON[state.theme], fg=colors.TEXT[state.theme], text=getTranslationKey(state.language, 'map.toCurrentWord'))
        self.lbl_page.config(bg=colors.BACKGROUND[state.theme], fg=colors.TEXT[state.theme])
        self.textw.config(bg=colors.DISPLAY[state.theme], fg=colors.TEXT[state.theme])
        self.frame.config(bg=colors.BACKGROUND[state.theme])
        self.mapframe.config(bg=colors.BACKGROUND[state.theme])
        self.textw.tag_configure('currentToken', background=colors.TEXT[state.theme], foreground=colors.TEXT[not state.theme])
        self.comlist.trigger('update-state', state)
