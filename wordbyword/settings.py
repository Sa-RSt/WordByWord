import json
import os

SETTINGS_FILE = os.path.expanduser('~/.wbwr_cfg')
DEFAULT_SETTINGS = {
    'blink_warning_shown': False,
    'night_mode': True,
    'speed': 300
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
