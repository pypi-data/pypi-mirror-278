traducciones = {
  'es': {
    'hola': 'hola',
    'adios': 'adios',
  },
  'en': {
    'hola': 'hello',
    'adios': 'bye',
  },
  'it': {
    'hola': 'ciao',
    'adios': 'arrivederci',
  }
}


def traducir(texto, lang='en'):
  if lang in traducciones:
    if texto in traducciones[lang]:
      return traducciones[lang][texto]
    else:
      return f'No podemos traducir el texto {texto} al {lang}'
  else:
    return f'No podemos traducir al {lang}'