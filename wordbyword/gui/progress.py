# -*- coding: utf-8 -*-

from . import UIComponent
from tkinter import Frame, Label, Button
from tkinter.ttk import Progressbar, Style
from . import colors
from ..internationalization import getTranslationKey


FRAME_WIDTH = 350
FRAME_HEIGHT = 110


class Progress(UIComponent):

    def __init__(self, tkparent, total, asset_manager):
        '''
        @param total: The total number of words/tokens.
        '''
        super(Progress, self).__init__()

        self._lang = 'en'
        self._nightmode = True
        self._asset_manager = asset_manager
        self._shown = True
        self.total = total
        self._last_interval = 0
        self.current = 0
        self.frame = Frame(tkparent, width=FRAME_WIDTH, height=FRAME_HEIGHT)

        self.btn_toggle = Button(self.frame, command=self.on_toggle)
        self.btn_toggle.grid(row=0, column=0)

        self.toggleframe = Frame(self.frame)

        self.style = Style(self.toggleframe)
        self.style.theme_use('clam')
        self.style.configure('wbwr.Horizontal.TProgressbar')

        self.progbar = Progressbar(self.toggleframe, mode='determinate', orient='horizontal', length=100, value=1, style='wbwr.Horizontal.TProgressbar')
        self.progbar.grid(row=0, column=0, sticky='nsew')

        self.lbl_progdata = Label(self.toggleframe)
        self.lbl_progdata.grid(row=0, column=1, sticky='nsew')

        self.toggleframe.grid(row=0, column=2)

        self.btn_save = Button(self.frame, command=lambda: self.trigger('save-progress'))
        self.btn_save.grid(row=0, column=1)

        msgf = Frame(self.frame)
        msgf.grid(row=1, column=0, columnspan=3)
        self.msg_saved = Label(msgf)
        self.msg_saved.grid(sticky='nsew')
        
        self.frame.grid_propagate(False)

        self.on('progress-saved', self.progress_saved)

        self.on('update-state', self.update_state)

    @property
    def shown(self):
        return self._shown
    
    @shown.setter
    def shown(self, val):
        theme = self._asset_manager.theme(self._nightmode)
        if val:
            self.toggleframe.grid(row=0, column=2)
            self.update(self._last_interval)
            self.btn_toggle.config(image=theme.get_prefixed_image('unsee.png'))
        else:
            self.toggleframe.grid_forget()
            self.btn_toggle.config(image=theme.get_prefixed_image('see.png'))

        self._shown = val

    @property
    def current(self):
        return self._current

    @current.setter
    def current(self, val):
        self._current = val

    @property
    def total(self):
        return self._total

    @total.setter
    def total(self, val):
        self._total = val

    def on_toggle(self):
        self.shown = not self.shown

    def update(self, interval):
        '''
        Update the progress UI.

        @param interval: The interval at which the display is being updated, in milliseconds.
        '''

        self._last_interval = interval
        if self.shown:
            percent = 100*(self.current+1)/(1+self.total)
            self.lbl_progdata.config(text='({:.1f}%)'.format(percent))
            self.progbar.config(value=int(percent))
            
            #remaining = self.total - self.current
            #words_per_second = 1000/interval
            # Since words with punctuation are displayed 1.75x longer,
            # multiplying by 1.3 will give us a rough estimate.
            #eta = 1.3 * remaining / words_per_second

            #self.lbl_eta.config(text='ETA: {}'.format(_timeformat(eta)))

    def progress_saved(self):
        theme = self._asset_manager.theme(self._nightmode)

        def restore():
            self.btn_save.config(image=theme.get_prefixed_image('save.png'))
            self.msg_saved.config(text='')


        self.btn_save.config(image=theme.get_prefixed_image('save_ok.png'))
        self.msg_saved.config(text=getTranslationKey(self._lang, 'progress.didSaveProgress'))
        self.frame.after(500, restore)

    def update_state(self, state):
        self._lang = state.language
        self._nightmode = state.theme
        self.shown = self.shown  # Update show/hide button's images (theme is considered here)

        theme = self._asset_manager.theme(self._nightmode)

        self.frame.config(bg=colors.BACKGROUND[state.theme])
        self.toggleframe.config(bg=colors.BACKGROUND[state.theme])
        self.msg_saved.config(bg=colors.BACKGROUND[state.theme], fg=colors.TEXT[state.theme])
        self.lbl_progdata.config(bg=colors.BACKGROUND[state.theme], fg=colors.TEXT[state.theme])
        self.btn_save.config(image=theme.get_prefixed_image('save.png'))
        self.style.configure('wbwr.Horizontal.TProgressbar', background=colors.TEXT[state.theme], troughcolor=colors.DISPLAY[state.theme])

    def get_tk_widget(self):
        return self.frame
