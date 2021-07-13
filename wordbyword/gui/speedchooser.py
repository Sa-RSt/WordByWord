from tkinter import Frame, Label, IntVar, Scale
from . import colors
from . import UIComponent


class SpeedChooser(UIComponent):
    def __init__(self, tkparent):

        super(SpeedChooser, self).__init__()

        self.frame = Frame(tkparent)

        self.label = Label(self.frame, text='Words per minute: ')
        self.label.grid(row=0, column=0)

        self.scale = Scale(self.frame, from_=60, to=600, command=self._command, orient='horizontal')
        self.scale.set(300)
        self.scale.grid(row=0, column=1)

        self.on('nightmode-state', self.update_nightmode_state)
    
    def _command(self, _):
        self.trigger('speed-change')

    @property
    def interval(self):
        '''
        Return the interval at which the words
        should be updated, in milisseconds.
        '''
        words_per_min = self.scale.get()
        words_per_sec = words_per_min / 60
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
        words_per_min = words_per_sec * 60
        self.scale.set(words_per_min)


    def update_nightmode_state(self, enabled):
        self.frame.config(bg=colors.BACKGROUND[enabled])
        self.label.config(bg=colors.BACKGROUND[enabled], fg=colors.TEXT[enabled])
        self.scale.config(bg=colors.BACKGROUND[enabled], fg=colors.TEXT[enabled], troughcolor=colors.DISPLAY[enabled])
        

    def get_tk_widget(self):
        return self.frame
