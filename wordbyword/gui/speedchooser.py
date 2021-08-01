# -*- coding: utf-8 -*-

from tkinter import Frame, Label, IntVar, Scale
from wordbyword.internationalization import getTranslationKey
from . import colors
from . import UIComponent


class SpeedChooser(UIComponent):
    def __init__(self, tkparent):

        super(SpeedChooser, self).__init__()

        self.frame = Frame(tkparent)

        self.label = Label(self.frame, text='Words per minute: ')
        self.label.grid(row=0, column=0)

        self.scale = Scale(self.frame, from_=60, to=600, command=self._command, orient='horizontal', length=150)
        self.scale.grid(row=0, column=1)

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
        return self.scale.get()
    
    @speed.setter
    def speed(self, val):
        self.scale.set(val)

    def update_state(self, state):
        self.frame.config(bg=colors.BACKGROUND[state.theme])
        self.label.config(bg=colors.BACKGROUND[state.theme], fg=colors.TEXT[state.theme], text=getTranslationKey(state.language, 'speedChooser.wordsPerMinute'))
        self.scale.config(bg=colors.BACKGROUND[state.theme], fg=colors.TEXT[state.theme], troughcolor=colors.DISPLAY[state.theme])
        

    def get_tk_widget(self):
        return self.frame
