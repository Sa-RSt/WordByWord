# -*- coding: utf-8 -*-

from math import copysign
from re import compile, fullmatch
from time import perf_counter
from tkinter import Frame, Button, Menu
from tkinter.filedialog import asksaveasfilename
from tkinter.messagebox import showerror, askyesnocancel, showwarning

from ..file_formats import check_extension, File, IMAGE_ANNO
from ..file_formats.jwbw import JWBWFileIO
from ..file_formats.read_file import read_file
from ..tokenization import split_tokens
from . import UIComponent
from .buttons import ButtonsComponent
from .display import Display
from .filepicker import Filepicker
from .map import Map
from .message_dialog import MessageDialog
from .progress import Progress
from .speedchooser import SpeedChooser
from .settings_menu import SettingsMenu
from .view_menu import ViewMenu
from .about_menu import AboutMenu
from .language_menu import LanguageChooser
from .font_size_slider import FontSizeSlider
from . import colors
from ..settings import Settings
from ..internationalization import getTranslationKey, SUPPORTED_LANGUAGES
from ..assets import AssetManager
from .state import State

DEFAULT_TEXT = 'The quick brown fox jumped over the lazy dog.'
NON_WORD_START = compile(r'^\W')
NON_WORD_END = compile(r'\W$')

def has_punctuation_or_line_break(word):
    '''
    Check if the given word has any
    punctuation characters.
    '''
    return NON_WORD_END.search(word) or NON_WORD_START.search(word)

class App(UIComponent):
    def __init__(self, tkparent, root_window, assets_path, filename):
        super(App, self).__init__()

        self._asset_manager = AssetManager(assets_path)

        self._state = State(theme=Settings['theme'], language=Settings['language'], font=Settings['font'])
        self._previous_offset = 1
        self._focus_mode = False

        self.root_window = root_window

        self.menu = Menu(root_window)

        self.language_chooser = LanguageChooser(self.menu, SUPPORTED_LANGUAGES)
        self.language_chooser.on('language', lambda language: self.update_state(State(theme=self._state.theme, language=language, font=self._state.font)))
        self.menu.add_cascade(label='Change Language/Mudar Idioma', menu=self.language_chooser.get_tk_widget())

        self.settings_menu = SettingsMenu(self.menu, 2, Settings['pause_on_image'])
        self.settings_menu.on('nightmode-state', lambda theme: self.update_state(State(theme=theme, language=self._state.language, font=self._state.font)))
        self.settings_menu.on('font-changed', lambda font: self.update_state(State(theme=self._state.theme, language=self._state.language, font=font)))
        self.settings_menu.on('pause-on-image-cfg', self.pause_on_image_cfg)
        self.menu.add_cascade(**self.settings_menu.to_menu_cascade())

        self.view_menu = ViewMenu(self.menu, 3)
        self.view_menu.on('view-mode', self.view_mode_update)
        self.menu.add_cascade(**self.view_menu.to_menu_cascade())

        self.about_menu = AboutMenu(self.menu, 4)
        self.menu.add_cascade(**self.about_menu.to_menu_cascade())

        root_window.config(menu=self.menu)

        self.frame = Frame(tkparent)

        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(3, weight=1)

        self.progress = Progress(self.frame, len(split_tokens(DEFAULT_TEXT)), self._asset_manager)
        self.progress.get_tk_widget().grid(row=0, column=1, sticky='n')
        self.progress.on('save-progress', self.save_progress)

        self.speed_chooser = SpeedChooser(self.frame)
        self.speed_chooser.get_tk_widget().grid(row=0, column=2, sticky='ne')
        self.speed_chooser.speed = Settings['speed']
        self.speed_chooser.chars_per_frame = Settings['cpf']
        self.speed_chooser.on('speed-change', self.on_speed_change)

        self.filepicker = Filepicker(self.frame)
        self.filepicker.get_tk_widget().grid(row=0, column=0, sticky='nw')
        self.filepicker.on('file-change', self.get_file)
        self.filepicker.on('will-pick-file', self.will_pick_file)

        self.display = Display(self.frame, Settings['font_size_focus'])
        self.display.on('double-click', lambda: self.view_menu.toggle_focus())
        self.display.get_tk_widget().grid(row=1, column=0, columnspan=3)

        self.buttons = ButtonsComponent(self.frame, self._asset_manager)
        self.buttons.get_tk_widget().grid(row=2, column=0, columnspan=3)

        self.map = Map(self.frame)
        self.map.on('token-change', self.token_change)
        self.map.get_tk_widget().grid(row=3, column=0, columnspan=3)
        
        self.font_size_slider = FontSizeSlider(self.frame, self._asset_manager, Settings['font_size_focus'])
        self.font_size_slider.propagate_event_to('font-size-change', self.display)
        self.font_size_slider.on('font-size-change', self._save_font_size)

        self.frame.after(self.speed_chooser.interval, self.updateloop)

        self.set_contents(DEFAULT_TEXT)
        self.position = 0

        self.root_window.protocol('WM_DELETE_WINDOW', self.on_quit_button)
        self.root_window.bind('<space>', lambda _: self.buttons.onpause())
        self.root_window.bind('<Control-f>', lambda _: self.map.on_find())
        self.root_window.bind('<Control-F>', lambda _: self.map.on_go_to_page())
        self.root_window.bind('<Control-g>', lambda _: self.map.on_scroll_to_current())
        self.root_window.bind('<F11>', lambda _: self.view_menu.toggle_fullscreen())
        self.root_window.bind('<Escape>', self.on_esc)

        if filename is not None:
            self.filepicker.filename = filename
        
        self.update_state(self._state)
        self.settings_menu.nightmode_toggle.enabled = Settings['theme']

        if not Settings['blink_warning_shown']:
            self.about_menu.show_health_and_safety_warning()
            Settings['blink_warning_shown'] = True
            Settings.save()
    
    def _save_font_size(self, sz):
        Settings['font_size_focus'] = sz

    def view_mode_update(self, viewmode):
        fullscreen, focus = viewmode
        self.root_window.attributes('-fullscreen', fullscreen)

        if focus != self._focus_mode:
            self._focus_mode = focus
            self.display.trigger('focus-mode', focus)
            if focus:
                self.map.get_tk_widget().grid_forget()
                self.font_size_slider.get_tk_widget().grid(row=3, column=0, columnspan=4, pady=(10, 0))
            else:
                self.map.get_tk_widget().grid(row=3, column=0, columnspan=3)
                self.font_size_slider.get_tk_widget().grid_forget()

    def on_esc(self, *_, **__):
        self.root_window.attributes('-fullscreen', False)
        self.view_menu.fullscreen.set(False)

    def token_change(self, position):
        self.position = position - 1  # Position will increase by 1 on update.
        self.update_display(1)
    
    def updateloop(self):
        start = perf_counter()

        if not self.buttons.paused:
            self._previous_offset = self.update_display(self._previous_offset)
        
        elapsed = perf_counter() - start
        self.frame.after(int((self.speed_chooser.interval - elapsed*1000) / abs(self.buttons.factor)), self.updateloop)

    def update_display(self, offset):
        newpos = int(self.position + copysign(offset, self.buttons.factor))
        if newpos < len(self.tokens) and newpos >= 0:
            self.position = newpos
            self.progress.current = self.position
            toks_to_display = []
            content = ''
            for tok in range(self.position, len(self.tokens)):
                if toks_to_display and len(content + ' ' + self.tokens[tok].word) - 1 > self.speed_chooser.chars_per_frame:
                    break
                toks_to_display.append(self.tokens[tok])
                content += self.tokens[tok].word + ' '
                if has_punctuation_or_line_break(self.tokens[tok].word):
                    break
            if toks_to_display:
                self.map.current_token = toks_to_display[0]
            content = content[:-1]
            self.display.content = content
            if Settings['pause_on_image'] and content.strip() == IMAGE_ANNO:
                self.buttons.paused = True
            self.progress.update(self.speed_chooser.interval)
            return len(toks_to_display)
        return 1

    def will_pick_file(self):
        if not self.filepicker.filename:
            return
        ans = askyesnocancel(getTranslationKey(self._state.language, 'confirmSave.title'), getTranslationKey(self._state.language, 'confirmSave.body'))
        if ans is None:
            return True
        elif ans:
            self.save_progress()

    def get_file(self, filename):
        if not filename:
            return
        mbox = MessageDialog(self.get_tk_widget(), getTranslationKey(self._state.language, 'converting.title'), getTranslationKey(self._state.language, 'converting.body'))
        try:
            try:
                content = read_file(filename)
            except Exception as exc:
                self.filepicker.filename = ''
                showerror(
                    getTranslationKey(self._state.language, 'error.readFile.title'),
                    getTranslationKey(self._state.language, 'error.readFile.body').format(str(exc))
                )
                return
            if content is not None:
                self.set_contents(content.text)
                self.position = content.current_word
                self.map.comlist.load_comments(content.comments)
                self.update_display(1)
                
        finally:
            mbox.destroy()

    def set_contents(self, contents):
        self.map.text = contents       # Map tokenizes the text automatically
        self.tokens = self.map.tokens  #
        self.progress.total = len(self.tokens)
        self.position = -1  # self.update_display increments the position, so it will be set to 0
                            # after the first update.
        self.buttons.paused = True
        self.update_display(1)
    
    def save_progress(self):
        fname = self.filepicker.filename
        if check_extension(fname, '.jwbw'):
            self.create_jwbw(fname)
            self.progress.trigger('progress-saved')
        else:
            output = asksaveasfilename(filetypes=[(getTranslationKey(self._state.language, 'fileType.jwbw'), '.jwbw')], defaultextension='.jwbw')
            if output:
                self.create_jwbw(output)
                self.filepicker.filename = output
                self.save_progress()

    def create_jwbw(self, fname):
        cw = max(self.position - 1, 0)  # Position will be incremented on each update
        fio = JWBWFileIO()
        fio.write(fname, File(text=self.map.text, current_word=cw, comments=self.map.comlist.dump_comments()))

    def pause_on_image_cfg(self, will_pause):
        Settings['pause_on_image'] = will_pause

    def on_speed_change(self):
        self.progress.update(self.speed_chooser.interval)
        Settings['speed'] = self.speed_chooser.speed
        Settings['wpf'] = self.speed_chooser.chars_per_frame

    def on_quit_button(self):
        self.buttons.paused = True
        fname = self.filepicker.filename

        if not fname.strip():
            self.terminate_app()
            return None

        self.save_or_confirm_quit()    

    def save_or_confirm_quit(self):
        ans = askyesnocancel(getTranslationKey(self._state.language, 'confirmSave.title'), getTranslationKey(self._state.language, 'confirmSave.body'))
        if ans is True:
            self.save_progress()
            self.terminate_app()
        elif ans is False:
            self.terminate_app()
        
    def terminate_app(self):
        '''Exit the program.'''
        self.root_window.destroy()
        
    def update_state(self, state):
        self._state = state
        Settings['theme'] = state.theme
        Settings['language'] = state.language
        Settings['font'] = state.font
        Settings.save()

        children = [
            self.progress, self.speed_chooser, self.filepicker,
            self.display, self.buttons, self.map, self.settings_menu,
            self.view_menu, self.about_menu, self.font_size_slider
        ]

        self.frame.config(bg=colors.BACKGROUND[state.theme])
        for comp in children:
            comp.trigger('update-state', state)
        
        self.root_window.update()

    def get_tk_widget(self):
        return self.frame

