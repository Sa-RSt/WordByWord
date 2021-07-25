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

        self.textw = Text(self.frame, width=40, height=4)
        self.textw.bind('<FocusIn>', self._hightlight)
        self.textw.bind('<Button-1>', self._hightlight)
        self.textw.bind('<FocusOut>', lambda x: self.trigger('highlight', None))
        self.textw.grid(row=0, column=0, columnspan=11)

        self.span = span

        self.btn_del = Button(self.frame, text='×', command=self.on_btn_del)
        self.btn_del.grid(row=0, column=12)

        self.on('nightmode-state', self.update_nightmode_state)

    @property
    def text(self):
        return self.textw.get('1.0', 'end')
    
    @text.setter
    def text(self, val):
        self.textw.delete('1.0', 'end')
        self.textw.insert('1.0', val)

    def on_btn_del(self):
        self.trigger('destroy', self)
    
    def _hightlight(self, *_):
        self.trigger('highlight', self.span)

    def update_nightmode_state(self, enabled):
        self.textw.config(bg=colors.CONTROL_BUTTON[enabled], fg=colors.TEXT[enabled], insertbackground=colors.TEXT[enabled])
        self.btn_del.config(bg='red', fg='white')
        self.frame.config(bg=colors.BACKGROUND[enabled])

    def get_tk_widget(self):
        return self.frame


class CommentList(UIComponent):
    def __init__(self, tkparent):
        super(CommentList, self).__init__()

        self._comments = []
        self._currentRow = 0
        self._currentSelection = None
        self._nightmode = False

        self.frame = Frame(tkparent)

        self.btn_add = Button(self.frame, text='[+] Add comment/bookmark', command=self.on_add)
        self.btn_add.grid(row=0, column=0, sticky='new')

        self.sf = ScrolledFrame(self.frame, scrollbars='vertical')
        self.sf.grid(row=1, column=0, rowspan=15, sticky='nsew')
        self.comframe = self.sf.display_widget(Frame, True)

        self.frame.grid_rowconfigure(1, weight=1)

        self.on('update-selection', self.update_selection)
        self.on('nightmode-state', self.update_nightmode_state)
    
    def add_comment(self, span):
        com = Comment(self.comframe, span)
        com.get_tk_widget().grid(row=self._currentRow, column=0)
        com.trigger('nightmode-state', self._nightmode)
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
            showerror('Word by Word Reader', 'Please use your cursor to select some text to comment on')
            return
        self.add_comment(self._currentSelection)

    def update_selection(self, selspan):
        self._currentSelection = selspan

    def get_tk_widget(self):
        return self.frame
    
    def update_nightmode_state(self, enabled):
        self._nightmode = enabled
        self.frame.config(bg=colors.BACKGROUND[enabled])
        self.comframe.config(bg=colors.BACKGROUND[enabled])
        self.sf.config(bg=colors.BACKGROUND[enabled])
        self.sf._canvas.config(bg=colors.BACKGROUND[enabled])
        self.btn_add.config(bg=colors.BUTTON[enabled], fg=colors.TEXT[enabled])
        for com in self._comments:
            com.trigger('nightmode-state', enabled)
