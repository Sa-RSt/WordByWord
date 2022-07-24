# -*- coding: utf-8 -*-

# A dict with the currently supported languages.
# The keys are the two-letter language codes, and the values are
# the human readable names of the languages.
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'pt': 'Português'
}

about_en = '''
This app, better suited for non-fiction content, intends to boost the user's focus and reading speed.

Copyright © Samuel R. Steidle
'''.strip()

about_pt = '''
Esse programa, que é mais adequado a conteúdo de não-ficção, tem como objetivo aumentar o foco do usuário e sua velocidade de leitura.

Copyright © Samuel R. Steidle
'''.strip()

_keys = {
    ### [ Global ] ###
    'ok': {
        'en': 'OK',
        'pt': 'OK'
    },
    'cancel': {
        'en': 'Cancel',
        'pt': 'Cancelar'
    },
    ### [ Menus ] ###
    'menu.settings': {
        'en': 'Settings',
        'pt': 'Configurações'
    },
    'menu.about': {
        'en': 'About',
        'pt': 'Sobre'
    },
    ### [ View menu ] ###
    'menu.view': {
        'en': 'View',
        'pt': 'Visualizar'
    },
    'view.fullscreen': {
        'en': 'Fullscreen mode (F11)',
        'pt': 'Modo tela cheia (F11)'
    },
    'view.focus': {
        'en': 'Focus mode (double-click the word display)',
        'pt': 'Modo focado (duplo-clique no mostrador de palavras)'
    },
    ### [ About ] ###
    'about.menu': {
        'en': 'About WordByWord',
        'pt': 'Sobre o WordByWord'
    },
    'about.body': {
        'en': about_en,
        'pt': about_pt
    },
    ### [ Health & Safety ] ###
    'healthAndSafety.buttonText': {
        'en': 'Health & Safety Warning',
        'pt': 'Aviso de Saúde e Segurança'
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
    ### [ Image display ] ###
    'image.redirect': {
        'en': '\u23a3Use an external PDF reader to view the image\u23a4',
        'pt': '\u23a3Visualize a imagem em um leitor de PDF externo\u23a4'
    },
    ### [ Map ] ###
    'map.toCurrentWord': {
        'en': 'Scroll to current word (Ctrl+V)',
        'pt': 'Visualizar a palavra atual (Ctrl+V)'
    },
    'map.currentPage': {
        'en': 'Page: {}/{}',
        'pt': 'Página: {}/{}'
    },
    'map.addComment': {
        'en': '[+] Add comment/bookmark',
        'pt': '[+] Adicionar comentário'
    },
    'map.addComment.noneSelected': {
        'en': 'Please use your cursor to select some text to comment on.',
        'pt': 'Por favor, use seu cursor para selecionar o trecho de texto em que você deseja comentar.'
    },
    ### [ Find word ] ###
    'map.find.button': {
        'en': 'Find word... (Ctrl+F)',
        'pt': 'Encontrar palavra... (Ctrl+F)'
    },
    'map.find.title': {
        'en': 'Find word - Word by Word Reader',
        'pt': 'Encontrar palavra - Word by Word Reader'
    },
    'map.find.prev': {
        'en': 'Previous',
        'pt': 'Anterior'
    },
    'map.find.next': {
        'en': 'Next',
        'pt': 'Próxima'
    },
    'map.find.occurrences': {
        'en': 'Occurrences: {}/{}',
        'pt': 'Ocorrências: {}/{}'
    },
    'map.find.nowords': {
        'en': 'No occurrences were found.',
        'pt': 'Nenhuma ocorrência foi encontrada.'
    },
    ### [ Go to page ] ###
    'map.goToPage.button': {
        'en': 'Jump to page... (Ctrl+Shift+F)',
        'pt': 'Ir para página... (Ctrl+Shift+F)'
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
    'speedChooser.framesPerMinute': {
        'en': 'Chunks per minute: ',
        'pt': 'Chunks por minuto: '
    },
    'speedChooser.wordsPerFrame': {
        'en': 'Characters per chunk: ',
        'pt': 'Caracteres por chunk: '
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
    ### [ Tooltips ] ###
    'tt.fastRewind': {
        'en': 'Rewind (fast)',
        'pt': 'Retroceder (rápido)'
    },
    'tt.slowRewind': {
        'en': 'Rewind (slow)',
        'pt': 'Retroceder (lento)'
    },
    'tt.fastForward': {
        'en': 'Fast forward',
        'pt': 'Avançar rapidamente'
    },
    'tt.slowForward': {
        'en': 'Slow down',
        'pt': 'Avançar lentamente'
    },
    'tt.playOrPause': {
        'en': 'Play/pause',
        'pt': 'Pausar/reproduzir'
    },
    ### [ Theme toggle ] ###
    'themeToggle.changeTheme': {
        'en': 'Toggle night mode',
        'pt': 'Ativar/desativar modo noturno'
    },
    ### [ Font chooser ] ###
    'fontChooser.changeFont': {
        'en': 'Change font',
        'pt': 'Alterar fonte'
    },
    'fontChooser.label': {
        'en': 'Current font: {}',
        'pt': 'Fonte atual: {}'
    },
    ### [ Pause on image? ] ###
    'pauseOnImage.checkbox': {
        'en': 'Pause playback when an image is detected',
        'pt': 'Pausar reprodução quando uma imagem for detectada'
    }
}


def getTranslationKey(lang, key):
    '''Return the translated text for the given key in the language `lang`.'''
    return _keys[key][lang]

