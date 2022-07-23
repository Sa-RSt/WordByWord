# -*- coding: utf-8 -*-

import json
import os
from locale import getdefaultlocale
from .internationalization import SUPPORTED_LANGUAGES


_lang = getdefaultlocale()[0]
for _supported_lang in SUPPORTED_LANGUAGES.keys():
    if _lang in _supported_lang or _supported_lang in _lang:
        _lang = _supported_lang
        break
else:
    _lang = 'en'


SETTINGS_FILE = os.path.expanduser('~/.wbwr_cfg')
DEFAULT_SETTINGS = {
    'blink_warning_shown': False,
    'theme': 1,
    'speed': 125,
    'cpf': 20,
    'language': _lang,
    'font': 'serif',
    'pause_on_image': True,
    'font_size_focus': 45
}

class _settings_type(dict):
    def __getitem__(self, name):
        try:
            return super(_settings_type, self).__getitem__(name)
        except KeyError:
            val = DEFAULT_SETTINGS[name]
            self[name] = val
            return val

    def save(self):
        with open(SETTINGS_FILE, 'w') as file:
            json.dump(self, file)
    
    def load(self):
        self.clear()
        with open(SETTINGS_FILE, 'r') as file:
            for k, v in json.load(file).items():
                self[k] = v

Settings = _settings_type()
try:
    Settings.load()
except OSError:
    pass  # Settings will be populated and saved on demand
