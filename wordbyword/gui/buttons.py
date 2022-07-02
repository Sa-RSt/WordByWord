# -*- coding: utf-8 -*-

from . import UIComponent
from tkinter import Frame, Button
from ..assets import AssetManager

from . import colors

# Light theme and dark theme, respectively
BUTTON_HIGHLIGHT_COLOR = ('green', '#33ff33')


class ButtonsComponent(UIComponent):
    def __init__(self, tkparent, asset_manager: AssetManager):
        '''
        Initialize buttons.
        Arguments starting with on* must be callable objects
        to be called with no arguments when their respective
        buttons are pressed.
        '''
        super(ButtonsComponent, self).__init__()

        self._paused = False
        self._factor = 1
        self._nightmode = False
        self._asset_manager = asset_manager

        self.frame = Frame(tkparent)

        default_imgs = self._asset_manager.theme(self._nightmode)
        self.btn_rw_outer = Frame(self.frame)
        self.btn_rewind = Button(self.btn_rw_outer, image=default_imgs.get_prefixed_image('rewind.png'), command=self.onrewind)
        self.btn_rewind.grid(row=0, column=0, sticky='nsew', padx=2, pady=2)
        self.btn_rw_outer.grid(row=0, column=0, sticky='nsew')

        self.btn_srw_outer = Frame(self.frame)
        self.btn_slowrewind = Button(self.btn_srw_outer, image=default_imgs.get_prefixed_image('slow_rewind.png'), command=self.on05rewind)
        self.btn_slowrewind.grid(row=0, column=0, sticky='nsew', padx=2, pady=2)
        self.btn_srw_outer.grid(row=0, column=1, sticky='nsew')

        self.btn_pause = Button(self.frame, image=default_imgs.get_prefixed_image('pause.png'), command=self.onpause)
        self.btn_pause.grid(row=0, column=2, sticky='nsew')

        self.btn_sf_outer = Frame(self.frame)
        self.btn_slowforward = Button(self.btn_sf_outer, image=default_imgs.get_prefixed_image('slow_forward.png'), command=self.on05forward)
        self.btn_slowforward.grid(row=0, column=0, sticky='nsew', padx=2, pady=2)
        self.btn_sf_outer.grid(row=0, column=3, sticky='nsew')

        self.btn_ff_outer = Frame(self.frame)
        self.btn_fastforward = Button(self.btn_ff_outer, image=default_imgs.get_prefixed_image('fast_forward.png'), command=self.onfastforward)
        self.btn_fastforward.grid(row=0, column=0, sticky='nsew', padx=2, pady=2)
        self.btn_ff_outer.grid(row=0, column=4, sticky='nsew')

        self.on('update-state', self.update_state)
    
    @property
    def paused(self):
        return self._paused
    
    @paused.setter
    def paused(self, val):
        self._paused = val
        theme = self._asset_manager.theme(self._nightmode)
        if self.paused:
            self.btn_pause.config(image=theme.get_prefixed_image('play.png'))
        else:
            self.btn_pause.config(image=theme.get_prefixed_image('pause.png'))

    @property
    def factor(self):
        return self._factor
    
    @factor.setter
    def factor(self, val):
        self._factor = val
        factors_frames = {
             0.5: self.btn_sf_outer,
             2:   self.btn_ff_outer,
            -2:   self.btn_rw_outer,
            -0.5: self.btn_srw_outer,
        }

        for x in factors_frames.values():
            x.config(bg=colors.BACKGROUND[self._nightmode])

        if self._factor in factors_frames.keys():
            factors_frames[self._factor].config(bg=BUTTON_HIGHLIGHT_COLOR[self._nightmode])

    def get_tk_widget(self):
        return self.frame

    def onpause(self):
        self.paused = not self.paused
        self.factor = 1

    def on05forward(self):
        self.paused = False
        if self.factor == 0.5:
            self.factor = 1
        else:
            self.factor = 0.5
    
    def on05rewind(self):
        self.paused = False
        if self.factor == -0.5:
            self.factor = 1
        else:
            self.factor = -0.5

    def onfastforward(self):
        self.paused = False
        if self.factor == 2:
            self.factor = 1
        else:
            self.factor = 2

    def onrewind(self):
        self.paused = False
        if self.factor == -2:
            self.factor = 1
        else:
            self.factor = -2
    
    def update_state(self, state):
        self._nightmode = state.theme
        self.factor = self.factor  # Updates the colors of the outer frames

        theme_imgs = self._asset_manager.theme(state.theme)

        self.btn_fastforward.config(bg=colors.CONTROL_BUTTON[state.theme], image=theme_imgs.get_prefixed_image('fast_forward.png'))
        self.btn_pause.config(bg=colors.CONTROL_BUTTON[state.theme])
        self.paused = self.paused  # Automatically reconfigures play/pause button icon
        self.btn_rewind.config(bg=colors.CONTROL_BUTTON[state.theme], image=theme_imgs.get_prefixed_image('rewind.png'))
        self.btn_slowforward.config(bg=colors.CONTROL_BUTTON[state.theme], image=theme_imgs.get_prefixed_image('slow_forward.png'))
        self.btn_slowrewind.config(bg=colors.CONTROL_BUTTON[state.theme], image=theme_imgs.get_prefixed_image('slow_rewind.png'))
        self.frame.config(bg=colors.BACKGROUND[state.theme])
    
    
