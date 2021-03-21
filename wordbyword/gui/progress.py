from . import UIComponent
from tkinter import Frame, Label
from tkinter.ttk import Button, Progressbar


def _timeformat(seconds):
    '''
    Returns the given time, in seconds, formated as 'XXh YYm ZZs'.
    '''
    seconds = int(seconds)
    minutes = seconds // 60
    hours = minutes // 60
    minutes = minutes % 60
    seconds = seconds % 60
    if hours == 0:
        if minutes == 0:
            return '{}s'.format(seconds)
        else:
            return '{}m {}s'.format(minutes, seconds)
    else:
        return '{}h {}m {}s'.format(hours, minutes, seconds)

class Progress(UIComponent):

    def __init__(self, tkparent, total):
        '''
        @param total: The total number of words/tokens.
        '''
        super(Progress, self).__init__()

        self._shown = True
        self.total = total
        self._last_interval = 0
        self.current = 0
        self.frame = Frame(tkparent)

        self.btn_toggle = Button(self.frame, text='Hide progress', command=self.on_toggle)
        self.btn_toggle.grid(row=0, column=0)

        self.toggleframe = Frame(self.frame)

        self.progbar = Progressbar(self.toggleframe, mode='determinate', orient='horizontal', length=100, value=1)
        self.progbar.grid(row=0, column=0, sticky='nsew', columnspan=2)

        self.lbl_progdata = Label(self.toggleframe)
        self.lbl_progdata.grid(row=1, column=0, sticky='nsew')

        self.lbl_eta = Label(self.toggleframe)
        self.lbl_eta.grid(row=1, column=1, sticky='nsew')

        self.toggleframe.grid(row=1, column=0)
        self.frame.rowconfigure(1, weight=1)

    @property
    def shown(self):
        return self._shown
    
    @shown.setter
    def shown(self, val):
        if self._shown and not val:
            self.toggleframe.grid_remove()
            self.btn_toggle.config(text='Show progress')
        elif not self.shown and val:
            self.toggleframe.grid(row=1, column=0)
            self.update(self._last_interval)
            self.btn_toggle.config(text='Hide progress')

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
        This method should be called periodically,
        inside a loop.

        @param interval: The interval at which the display is being updated, in milliseconds.
        '''

        self._last_interval = interval
        if self.shown:
            percent = 100*(self.current+1)/self.total
            self.lbl_progdata.config(text='{}/{} ({:.1f}%)'.format(self.current+1, self.total, percent))
            self.progbar.config(value=int(percent))
            
            remaining = self.total - self.current
            words_per_second = 1000/interval
            # Since words with punctuation are displayed 1.75x longer,
            # multiplying by 1.3 will give us a rough estimate.
            eta = 1.3 * remaining / words_per_second

            self.lbl_eta.config(text='ETA: {}'.format(_timeformat(eta)))


    def get_tk_widget(self):
        return self.frame
