# -*- coding: utf-8 -*-

from tkinter import Frame, Label, Scale
from tkinter.ttk import Separator
from wordbyword.internationalization import getTranslationKey
from . import colors
from . import UIComponent


class SpeedChooser(UIComponent):
    def __init__(self, tkparent):

        super(SpeedChooser, self).__init__()

        self.frame = Frame(tkparent)

        self.label_fpm = Label(self.frame, text='Frames per minute: ')
        self.label_fpm.grid(row=0, column=0)

        self.scale_fpm = Scale(self.frame, from_=30, to=750, resolution=5, command=self._command, orient='horizontal', length=150)
        self.scale_fpm.grid(row=0, column=1)

        self.label_cpf = Label(self.frame, text='Characters per frame: ')
        self.label_cpf.grid(row=1, column=0)

        self.scale_cpf = Scale(self.frame, from_=1, to=60, resolution=1, command=self._command, orient='horizontal', length=150)
        self.scale_cpf.grid(row=1, column=1)

        self.on('update-state', self.update_state)
    
    def _command(self, _):
        self.trigger('speed-change')

    @property
    def interval(self):
        '''
        Return the interval at which the words
        should be updated, in milisseconds.
        '''
        words_per_sec = self.speed / 60
        delay_in_secs = 1/words_per_sec
        return int(delay_in_secs * 1000)
    
    @interval.setter
    def interval(self, val):
        '''
        Sets the spinbox's frequency based on the given
        interval in milisseconds.
        '''
        delay_in_secs = val/1000
        words_per_sec = 1/delay_in_secs
        self.speed = words_per_sec * 60

    @property
    def speed(self):
        return self.scale_fpm.get()
    
    @speed.setter
    def speed(self, val):
        self.scale_fpm.set(val)

    @property
    def chars_per_frame(self):
        return self.scale_cpf.get()

    @chars_per_frame.setter
    def chars_per_frame(self, val):
        self.scale_cpf.set(val)

    def update_state(self, state):
        self.frame.config(bg=colors.BACKGROUND[state.theme])
        self.label_fpm.config(bg=colors.BACKGROUND[state.theme], fg=colors.TEXT[state.theme], text=getTranslationKey(state.language, 'speedChooser.framesPerMinute'))
        self.scale_fpm.config(bg=colors.BACKGROUND[state.theme], fg=colors.TEXT[state.theme], troughcolor=colors.DISPLAY[state.theme])

        self.label_cpf.config(bg=colors.BACKGROUND[state.theme], fg=colors.TEXT[state.theme], text=getTranslationKey(state.language, 'speedChooser.wordsPerFrame'))
        self.scale_cpf.config(bg=colors.BACKGROUND[state.theme], fg=colors.TEXT[state.theme], troughcolor=colors.DISPLAY[state.theme])
        

    def get_tk_widget(self):
        return self.frame
