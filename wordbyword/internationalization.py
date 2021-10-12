# -*- coding: utf-8 -*-

# A dict with the currently supported languages.
# The keys are the two-letter language codes, and the values are
# the human readable names of the languages.
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'pt': 'Português'
}

_keys = {
    ### [ Health & Safety ] ###
    'healthAndSafety.buttonText': {
        'en': 'HEALTH & SAFETY WARNING',
        'pt': 'AVISO DE SAÚDE E SEGURANÇA'
    },
    'healthAndSafety.title': {
        'en': 'IMPORTANT HEALTH & SAFETY WARNING',
        'pt': 'IMPORTANTE: AVISO DE SAÚDE E SEGURANÇA'
    },
    'healthAndSafety.body': {
        'en': 'Just like any other app, excessive usage can make your eyes hurt. Please take a 10 to 15 minute break every hour, even if you don\'t think you need it. Also, it is VERY important not to forget to blink your eyes while reading.',
        'pt': 'Assim como qualquer outro programa de computador, o uso excessivo desse aplicativo pode ferir seus olhos. Por favor, faça pausas de 10 a 15 minutos a cada hora, mesmo que você não acredite que precise dessas pausas. Além disso, é MUITO importante não se esquecer de piscar enquanto lê.'
    },
    ### [ Confirm save ] ###
    'confirmSave.title': {
        'en': 'Save Progress - Word by Word reader',
        'pt': 'Salvar Progresso - Word by Word Reader'
    },
    'confirmSave.body': {
        'en': 'Would you like to save your progress, so you can resume reading later?',
        'pt': 'Você gostaria de salvar seu progresso, para conseguir voltar a ler do ponto em que parou?'
    },
    ### [ Loading dialog ] ###
    'converting.title': {
        'en': 'Word by Word Reader: Loading...',
        'pt': 'Word by Word Reader: Carregando...'
    },
    'converting.body': {
        'en': 'Converting file. Please wait. This may take several minutes...',
        'pt': 'Convertendo arquivo. Por favor, espere alguns minutos...'
    },
    ### [ Errors ] ###
    'error.readFile.title': {
        'en': 'Word by Word Reader - Error',
        'pt': 'Word by Word Reader - Erro'
    },
    'error.readFile.body': {
        'en': 'We are sorry for the inconvenience. Could not read file. Error details: {}',
        'pt': 'Sentimos muito pela inconveniência. Falha ao ler arquivo. Detalhes do erro: {}'
    },
    ### [ File picker ] ###
    'filePicker.pickAFile':{
        'en': 'Pick a file (.PDF or .TXT)...',
        'pt': 'Escolher arquivo (.PDF ou .TXT)...'
    },
    'fileType.*': {
        'en': 'Files',
        'pt': 'Arquivos'
    },
    'fileType.jwbw': {
        'en': 'Word by Word Reader progress files',
        'pt': 'Arquivos de progresso do Word by Word Reader'
    },
    'fileType.txt': {
        'en': 'Text files',
        'pt': 'Documentos de texto'
    },
    'fileType.pdf': {
        'en': 'PDF books',
        'pt': 'Livros PDF'
    },
    'fileType.wbwr': {
        'en': 'Word by Word Reader legacy files',
        'pt': 'Arquivos de progresso do Word by Word Reader'
    },
    ### [ Map ] ###
    'map.toCurrentWord': {
        'en': 'Scroll to current word',
        'pt': 'Visualizar a palavra atual'
    },
    'map.currentPage': {
        'en': 'Page: {}/{}',
        'pt': 'Página: {}/{}'
    },
    'map.addComment': {
        'en': '[+] Add comment/bookmark (or right-click with your mouse)',
        'pt': '[+] Adicionar comentário (ou use o botão direito do mouse)'
    },
    'map.addComment.noneSelected': {
        'en': 'Please use your cursor to select some text to comment on.',
        'pt': 'Por favor, use seu cursor para selecionar o trecho de texto em que você deseja comentar.'
    },
    ### [ Find word ] ###
    'map.find.button': {
        'en': 'Find word...',
        'pt': 'Encontrar palavra...'
    },
    'map.find.title': {
        'en': 'Find word - Word by Word Reader',
        'pt': 'Encontrar palavra - Word by Word Reader'
    },
    'map.find.body': {
        'en': 'Search for word or press ENTER to jump to the next occurence:',
        'pt': 'Procure pela palavra ou pressione ENTER para ir à próxima ocorrência:'
    },
    ### [ Go to page ] ###
    'map.goToPage.button': {
        'en': 'Jump to page...',
        'pt': 'Ir para página...'
    },
    'map.goToPage.title': {
        'en': 'Jump to Page - Word by Word Reader',
        'pt': 'Ir para página - Word by Word Reader'
    },
    'map.goToPage.body': {
        'en': 'Current page: {}/{} | Enter the number of the page below:',
        'pt': 'Página atual: {}/{} | Insira o número da página abaixo:'
    },
    ### [ Speed chooser ] ###
    'speedChooser.wordsPerMinute': {
        'en': 'Words per minute: ',
        'pt': 'Palavras por minuto: '
    },
    ### [ Progress ] ###
    'progress.showProgress': {
        'en': 'Show progress',
        'pt': 'Exibir progresso'
    },
    'progress.hideProgress': {
        'en': 'Hide progress',
        'pt': 'Ocultar progresso'
    },
    'progress.saveProgress': {
        'en': 'Save progress',
        'pt': 'Salvar progresso'
    },
    'progress.didSaveProgress': {
        'en': 'Successfully saved!',
        'pt': 'Salvo com sucesso!'
    },
    ### [ Theme toggle ] ###
    'themeToggle.lightTheme': {
        'en': 'Light theme',
        'pt': 'Tema claro'
    },
    'themeToggle.darkTheme': {
        'en': 'Dark theme',
        'pt': 'Tema escuro'
    }
}


def getTranslationKey(lang, key):
    '''Return the translated text for the given key in the language `lang`.'''
    return _keys[key][lang]

