import json
import os

SETTINGS_FILE = os.path.expanduser('~/.wbwr_cfg')

class _settings_type(dict):
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
    Settings['version'] = 1
    Settings['night_mode'] = True
    Settings.save()
