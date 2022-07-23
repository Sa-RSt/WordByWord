from tkinter import Frame, Button, Scale

from . import colors
from . import UIComponent

MIN = 20
MAX = 70

class FontSizeSlider(UIComponent):
    def __init__(self, tkparent, asset_manager, sz):
        super(FontSizeSlider, self).__init__()
        self.frame = Frame(tkparent)
        self._asset_manager = asset_manager

        self.scale = Scale(self.frame, from_=MIN, to=MAX, resolution=1, orient='horizontal', length=200, showvalue=False, command=self._command)
        self._btn_zoom_in = Button(self.frame, command=self._side_button_callback(+1))
        self._btn_zoom_out = Button(self.frame, command=self._side_button_callback(-1))

        self._btn_zoom_out.grid(row=0, column=0, sticky='nsew')
        self.scale.grid(row=0, column=1, columnspan=5, sticky='ew')
        self._btn_zoom_in.grid(row=0, column=6, sticky='nsew')

        self.on('update-state', self.update_state)

        self.scale.set(sz)  # Implicitly triggers _command and the 'font-size-change' event

    def _command(self, val):
        self.trigger('font-size-change', int(val))
    
    def _side_button_callback(self, amount):
        def _fun():
            current = self.scale.get()
            new = current + amount
            if new > MAX:
                new = MAX
            elif new < MIN:
                new = MIN
            self.scale.set(new)
        return _fun

    def update_state(self, state):
        theme = self._asset_manager.theme(state.theme)
        self._btn_zoom_in.config(image=theme.get_prefixed_image('zoom_in.png'))
        self._btn_zoom_out.config(image=theme.get_prefixed_image('zoom_out.png'))

        self.frame.config(bg=colors.BACKGROUND[state.theme])

        self.scale.config(bg=colors.BACKGROUND[state.theme], fg=colors.TEXT[state.theme], troughcolor=colors.DISPLAY[state.theme])

    def get_tk_widget(self):
        return self.frame
