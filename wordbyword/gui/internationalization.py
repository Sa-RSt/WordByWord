# A dict with the currently supported languages.
# The keys are the two-letter language codes, and the values are
# the human readable names of the languages.
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'pt': 'Português'
}

_keys = dict()

def addTranslationKey(key, translations):
    '''`key` must be descriptive a string, in English, to index the text. `translations` must be a dictionary whose keys are two-letter language codes and the value is the text translated in the language of the respective key.'''
    if set(SUPPORTED_LANGUAGES.keys()) != set(translations.keys()):
        raise BaseException('Mismatch between supported and supplied languages', SUPPORTED_LANGUAGES, translations)

    _keys[key] = translations


def getTranslationKey(lang, key):
    '''Return the translated text for the given key in the language `lang`.'''
    return _keys[key][lang]
