from tkinter import Frame, Label, IntVar
from tkinter.ttk import Scale
from . import UIComponent


class SpeedChooser(UIComponent):
    def __init__(self, tkparent):

        super(SpeedChooser, self).__init__()

        self.frame = Frame(tkparent)

        Label(self.frame, text='Words per minute: ').grid(row=0, column=0)

        value_display_var = IntVar()
        value_display_var.set(300)

        self.scale = Scale(self.frame, from_=60, to=600, command=lambda val: value_display_var.set(int(float(val))))
        self.scale.set(300)
        self.scale.grid(row=0, column=1)

        Label(self.frame, textvariable=value_display_var).grid(row=0, column=2)
    
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

    def get_tk_widget(self):
        return self.frame
