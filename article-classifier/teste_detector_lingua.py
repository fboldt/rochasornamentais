import pandas as pd
import csv
from tqdm import tqdm
import langid
import langdetect
import polyglot
from polyglot.text import Text, Word
from polyglot.detect import Detector

def detection_langid(text):
    lingua = langid.classify(text)
    return lingua[0]

def lang_detect(text):
    lingua = langdetect.detect_langs(text)[0]
    lingua1 = lingua.lang
    return lingua1

def polyglot1(text):
    texto = Text(text)
    return texto.language.code

# Importando o arquivo do excel
xls_file = pd.ExcelFile('/dados/lista.xlsx')
xls_file

# Pegando todas as linhas do arquivo (nrows=10)
df = xls_file.parse('list-download', header=None)
df.columns = ["Título", "link", "Relevante", "link_corrigido", "Nada"]
df = df.drop(["Nada"], axis=1)

# Salvar dados que existem na pasta PDF
with open('/dados/linguas_pdf.csv', 'w', newline='') as file:
    for i in tqdm(range(len(df))):
        row = df.iloc[i,:]
        row[0] = row[0].replace("/", "_")
        #if row[0] in open('/dados/arquivos.csv').read(): # Verificar se é possível fazer o download do arquivo
        if row[0] not in open('/dados/linguas_pdf.csv').read() and row[0] in open('/dados/pdfs_baixados.csv').read(): # Verificar se o arquivo já não foi adicionado na lista
            
            lingua1 = detection_langid(row[0])
            lingua2 = lang_detect(row[0])       
            lingua3 = polyglot1(row[0])
            

            writer = csv.writer(file)
            writer.writerow([row[0], lingua1, lingua2, lingua3])
                    
