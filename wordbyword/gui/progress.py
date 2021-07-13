from . import UIComponent
from tkinter import Frame, Label, Button
from tkinter.ttk import Progressbar, Style
from . import colors


FRAME_WIDTH = 175
FRAME_HEIGHT = 110  # Height normally
FRAME_HEIGHT_COLLAPSED = 56  # Height when progress is hidden by the user


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
        self.frame = Frame(tkparent, width=FRAME_WIDTH, height=FRAME_HEIGHT)

        self.btn_toggle = Button(self.frame, text='Hide progress', command=self.on_toggle)
        self.btn_toggle.grid(row=0, column=0)

        self.toggleframe = Frame(self.frame)

        self.style = Style(self.toggleframe)
        self.style.theme_use('clam')
        self.style.configure('wbwr.Horizontal.TProgressbar')

        self.progbar = Progressbar(self.toggleframe, mode='determinate', orient='horizontal', length=100, value=1, style='wbwr.Horizontal.TProgressbar')
        self.progbar.grid(row=0, column=0, sticky='nsew', columnspan=2)

        self.lbl_progdata = Label(self.toggleframe)
        self.lbl_progdata.grid(row=1, column=0, sticky='nsew')

        self.lbl_eta = Label(self.toggleframe)
        self.lbl_eta.grid(row=1, column=1, sticky='nsew')

        self.toggleframe.grid(row=1, column=0)

        self.btn_save = Button(self.frame, text='Save progress', command=lambda: self.trigger('save-progress'))
        self.btn_save.grid(row=2, column=0)

        self.frame.rowconfigure(1, weight=1)

        self.on('progress-saved', self.progress_saved)

        self.frame.grid_propagate(False)

        self.on('nightmode-state', self.update_nightmode_state)

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
        if self.shown:
            self.frame.config(height=FRAME_HEIGHT)
        else:
            self.frame.config(height=FRAME_HEIGHT_COLLAPSED)

    def update(self, interval):
        '''
        Update the progress UI.

        @param interval: The interval at which the display is being updated, in milliseconds.
        '''

        self._last_interval = interval
        if self.shown:
            percent = 100*(self.current+1)/self.total
            self.lbl_progdata.config(text='({:.1f}%)'.format(percent))
            self.progbar.config(value=int(percent))
            
            remaining = self.total - self.current
            words_per_second = 1000/interval
            # Since words with punctuation are displayed 1.75x longer,
            # multiplying by 1.3 will give us a rough estimate.
            eta = 1.3 * remaining / words_per_second

            self.lbl_eta.config(text='ETA: {}'.format(_timeformat(eta)))

    def progress_saved(self):
        self.btn_save.config(text='Successfully saved!')
        self.frame.after(500, lambda: self.btn_save.config(text='Save progress'))

    def update_nightmode_state(self, enabled):
        self.frame.config(bg=colors.BACKGROUND[enabled])
        self.btn_toggle.config(bg=colors.BUTTON[enabled], fg=colors.TEXT[enabled])
        self.toggleframe.config(bg=colors.BACKGROUND[enabled])
        self.lbl_eta.config(bg=colors.BACKGROUND[enabled], fg=colors.TEXT[enabled])
        self.lbl_progdata.config(bg=colors.BACKGROUND[enabled], fg=colors.TEXT[enabled])
        self.btn_save.config(bg=colors.BUTTON[enabled], fg=colors.TEXT[enabled])
        self.style.configure('wbwr.Horizontal.TProgressbar', background=colors.TEXT[enabled], troughcolor=colors.DISPLAY[enabled])

    def get_tk_widget(self):
        return self.frame
