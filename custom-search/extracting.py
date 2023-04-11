import os
import pandas as pd
import tika 
import pdftotext
from articleclassifier.Util import analiser, filtering, lemmatization, TF_IDF_Dic, rank_TF_IDF, TOP_x, Histograma, rankeador, media_ranks
from tika import parser
import PyPDF2


def extract_tika():
    path = './download'

    arqs = (os.listdir(path))
    lista = []

    for arq in arqs:
        
        parsed = parser.from_file('./download/'+arq)
        pdf_file = parsed["content"]

        if pdf_file:
            aux = pdf_file.split('\n')
            _file = ''
            for x in aux:
                if x:
                    _file += x

            lista.append(_analiser(_file))

            # try:
            #     fl = arq.split('.')
            #     arquivo = open('./txt/' + fl[0] + '.txt', 'w')
            #     arquivo.write(_file)
            #     arquivo.close()
            # except Exception as exc:
            #     print(exc, '\n')
            #     continue

        #break
    return TF_IDF_Dic(lista)
        

def extract_pdftotext():
    path = './download/'

    arqs = (os.listdir(path))
    lista = []

    for arq in arqs:
        pdf = open(path + arq, 'rb')
        
        try:
            pdf_file = pdftotext.PDF(pdf)
            fl = arq.split('.')
            arquivo = open('./txt/' + fl[0] + '.txt', 'w')
            arquivo.write("\n\n".join(pdf_file))
            arquivo.close()
        except Exception as exc:
            print(exc, '\n')
            continue

        pdf.close()
        
        
def extract_PyPDF2():
    
    path = './download/'
    arqs = (os.listdir(path))
    
    for arq in arqs:
        arquivo = open(arq + '.txt', 'w')
        read_pdf = PyPDF2.PdfFileReader(open(path + arq, 'rb'))
        
        for i in range(read_pdf.numPages):
            pdf_get_page = read_pdf.getPage(i)
            arquivo.write(pdf_get_page.extractText())
        
        arquivo.close()        
        

def _analiser(t1):
    pdf_file_lemma = None
    t1 = t1.lower()
    language = TextBlob_lang_detc(t1)
    pdf_file_filtered = filtering(t1, language)

    if pdf_file_filtered:
        pdf_file_lemma = lemmatization(pdf_file_filtered, language)
        #lista.append(pdf_file_lemma)
    
    return pdf_file_lemma

    
lista_dicionarios = extract_tika()

dicionarios_organizados = rank_TF_IDF(lista_dicionarios)
dicionarios_organizados_top = TOP_x(dicionarios_organizados, 20)
dic_contagem = Histograma(dicionarios_organizados_top)
pd.set_option('display.max_rows', 50)
x = pd.DataFrame(list(dic_contagem.items()), columns=['Palavra', 'Quantidade no TopX'])
x.sort_values(by=['Quantidade no TopX'], ascending=False, inplace=True)
print(x)


lista_rank = rankeador(lista_dicionarios)
dic_media = media_ranks(lista_rank)
x2 = pd.DataFrame(list(dic_media.items()), columns=['Palavra', 'Media do rank'])
x2.sort_values(by=['Media do rank'], inplace=True)
print(x2)
