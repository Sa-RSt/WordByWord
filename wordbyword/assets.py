import os
from tkinter import PhotoImage


def _add_theme_prefix(is_nightmode, filename):
    '''Return <<< 'dark_' + filename >>> if is_nightmode is true, otherwise return <<< 'light_' + filename >>>'''
    if is_nightmode:
        return 'dark_{}'.format(filename)
    else:
        return 'light_{}'.format(filename)


class AssetManager:
    '''
    Manages access to data inside the "assets/" directory.
    '''
    def __init__(self, directory):
        self._loaded_assets = dict()
        self.directory = directory

    def theme(self, theme):
        '''Return Theme object that allows access to assets for a given theme'''
        return Theme(theme, self)
        

class Theme:
    '''
    Manages access to data used by a given theme inside the "assets/" directory.
    '''
    def __init__(self, theme, asset_manager):
        self._asset_manager = asset_manager
        self._theme = theme

    def get_prefixed_asset_path(self, filename):
        '''Return the absolute path to a given filename inside the assets folder.'''
        return os.path.abspath(os.path.join(self._asset_manager.directory, _add_theme_prefix(self._theme, filename)))

    def get_prefixed_image(self, filename):
        '''Return a tkinter.PhotoImage from an asset located in the assets folder, prepending 'dark_' to the file name if the UI is currently in dark theme, and prepending 'light_' otherwise.'''

        fullpath = self.get_prefixed_asset_path(filename)

        try:
            return self._asset_manager._loaded_assets[fullpath]
        except KeyError:
            pass

        pti = PhotoImage(file=fullpath)
        self._asset_manager._loaded_assets[fullpath] = pti
        return pti
