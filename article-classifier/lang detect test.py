import polyglot
from polyglot.text import Text, Word
from polyglot.detect import Detector

def polyglot(text):
    texto = Text(text)
    return texto.language.name

print(polyglot("Eu sou do Brasil."))

# text = Text("Bonjour, Mesdames.")
# print(text.language.name)