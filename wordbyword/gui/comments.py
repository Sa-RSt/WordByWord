# -*- coding: utf-8 -*-

from ..internationalization import getTranslationKey
from .state import State
from . import UIComponent
from tkinter import Frame, Button, Text
from tkscrolledframe import ScrolledFrame
from tkinter.messagebox import showerror
from . import colors


class Comment(UIComponent):
    def __hash__(self):
        return id(self)

    def __init__(self, tkparent, span):
        super(Comment, self).__init__()

        self.frame = Frame(tkparent)

        self.tframe = Frame(self.frame, width=335, height=75)
        self.textw = Text(self.tframe)
        self.textw.bind('<Button-1>', self._hightlight)
        self.textw.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.tframe.grid(row=0, column=0, columnspan=11)

        self.span = span

        self.btn_del = Button(self.frame, text='×', command=self.on_btn_del)
        self.btn_del.grid(row=0, column=12)

        self.on('update-state', self.update_state)

    @property
    def text(self):
        return self.textw.get('1.0', 'end')
    
    @text.setter
    def text(self, val):
        self.textw.delete('1.0', 'end')
        self.textw.insert('1.0', val)

    def on_btn_del(self):
        self.trigger('destroy', self)
        self.trigger('highlight', None)
    
    def _hightlight(self, *_):
        self.trigger('highlight', self.span)

    def update_state(self, state):
        self.textw.config(bg=colors.CONTROL_BUTTON[state.theme], fg=colors.TEXT[state.theme], insertbackground=colors.TEXT[state.theme], font=(state.font,))
        self.btn_del.config(bg='red', fg='white')
        self.frame.config(bg=colors.BACKGROUND[state.theme])

    def focus(self):
        self.textw.focus()

    def get_tk_widget(self):
        return self.frame


class CommentList(UIComponent):
    def __init__(self, tkparent):
        super(CommentList, self).__init__()

        self._comments = []
        self._currentRow = 0
        self._currentSelection = None
        self._nightmode = False
        self._lang = 'en'
        self._font = 'serif'

        self.frame = Frame(tkparent)

        self.btn_add = Button(self.frame, text='[+] Add comment/bookmark', command=self.on_add)
        self.btn_add.grid(row=0, column=0, sticky='new')

        self.sf = ScrolledFrame(self.frame, scrollbars='vertical')
        self.sf.grid(row=1, column=0, rowspan=15, sticky='nsew')
        self.comframe = self.sf.display_widget(Frame, True)

        self.frame.grid_rowconfigure(1, weight=1)

        self.on('update-selection', self.update_selection)
        self.on('update-state', self.update_state)
    
    def add_comment(self, span):
        com = Comment(self.comframe, span)
        com.get_tk_widget().grid(row=self._currentRow, column=0)
        com.focus()
        com.trigger('update-state', State(theme=self._nightmode, language=self._lang, font=self._font))
        com.on('highlight', self._bubble_highlight)
        com.on('destroy', self.del_comment)
        self._currentRow += 1
        self._comments.append(com)
        return com

    def dump_comments(self):
        '''Return a list of all comments, suitable for JSON serialization.'''
        L = []
        for com in self._comments:
            L.append([com.span, com.text])
        return L
    
    def load_comments(self, comments):
        '''Set comments to the given list of comments, which should be the output of CommentsList.dump_comments()'''
        for com in self._comments:
            self.del_comment(com)
        
        for comdata in comments:
            com = self.add_comment(comdata[0])
            com.text = comdata[1]

    def _bubble_highlight(self, span):
        self.trigger('highlight', span)

    def del_comment(self, com):
        self._comments.remove(com)
        com.get_tk_widget().destroy()

    def on_add(self):
        if self._currentSelection is None:
            showerror('Word by Word Reader', getTranslationKey(self._lang, 'map.addComment.noneSelected'))
            return
        self.add_comment(self._currentSelection)

    def update_selection(self, selspan):
        self._currentSelection = selspan

    def get_tk_widget(self):
        return self.frame
    
    def update_state(self, state):
        self._nightmode = state.theme
        self._lang = state.language
        self._font = state.font

        self.frame.config(bg=colors.BACKGROUND[state.theme])
        self.comframe.config(bg=colors.BACKGROUND[state.theme])
        self.sf.config(bg=colors.BACKGROUND[state.theme])
        self.sf._canvas.config(bg=colors.BACKGROUND[state.theme])
        self.btn_add.config(bg=colors.BUTTON[state.theme], fg=colors.TEXT[state.theme], text=getTranslationKey(state.language, 'map.addComment'))
        for com in self._comments:
            com.trigger('update-state', state)
