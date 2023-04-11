import numpy as np
import spacy
import math
from spacy_cld import LanguageDetector
from spacy.lang.en import English
from spacy.lang.pt import Portuguese

language_detector = LanguageDetector()
# nlp.add_pipe(language_detector)

# Retorna a língua da string
def analiser(text):
    nlp = spacy.load('en_core_web_sm',disable=['ner', 'textcat'])
    nlp.max_length = 15000000
    #Primeira parte: descobrir o idioma da string
    doc = nlp(text)
    language = doc._.languages
    return language 

from spacy.lang.en.stop_words import STOP_WORDS
from spacy.lang.pt.stop_words import STOP_WORDS

dic2 = {
    "en": spacy.load("en_core_web_sm", disable=['ner', 'textcat']), 
    "pt": spacy.load("pt_core_news_sm", disable=['ner', 'textcat'])
}

#Filtrar as Stop Words
def filtering(text, language):
    if language == ['en']:
        nlp = dic2['en']
    
    elif language == ['pt']:
        nlp = dic2['pt']

    else:
        #Casos em que a língua não é nem português nem inglês
        return None
    nlp.max_length = 15000000
    my_doc = nlp(text)
    # Create list of word tokens
    token_list = []
    for token in my_doc:
        token_list.append(token.text)
    # Create list of word tokens after removing stopwords
    filtered_sentence =[] 
    for word in token_list:
        lexeme = nlp.vocab[word]
        if lexeme.is_stop == False and lexeme.is_alpha == True:
            filtered_sentence.append(word)
    return filtered_sentence

#Pegar os lemmas
def lemmatization(lista, language):
    lemma_word = []
    text = " ".join(lista)
    
    if language == ['en']:
        nlp = dic2['en']
        doc = nlp(text)
        for token in doc:
            lemma_word.append(token.lemma_)
        return lemma_word
    
    elif language == ['pt']:
        nlp = dic2['pt']
        doc = nlp(text)
        for token in doc:
            lemma_word.append(token.lemma_)
        return lemma_word

#Fazer o dicionário
def dictionary(text):
    dic = {}
    language = analiser(text)
    dic["language"] = language
    lista = filtering(text, language)
    dic["filtered words"] = lista
    dic["lemmas"] = lemmatization(lista, language)
    return dic

def oddNumbers(start,end):
    resp = []
    for num in range(start, end + 1): 
    # checking condition 
        if num % 2 != 0: 
            resp.append(num)
    return resp


#FUNÇÃO DE TRATAR O TEXTO E CONTAR AS PALAVRAS

def TextCounter(_text):
    if type(_text) == str:
        _text = _text.split()
    aux = {}
    for i in _text:
        if i in aux:
            aux[i] +=1
        else:
            aux[i] = 1
    return aux


def Vectorize(_dicionary,_texts):
    vet = []
    for i in _texts:
        aux = np.zeros(len(_dicionary))
        for word in i:
            if word in _dicionary:
                _id = _dicionary[word]['id']
                aux[_id] = i[word]
        vet.append(aux)
    return vet

# Função que retorna um dicionário com o TF de cada palavra de um determinado texto,
# onde a chave é a palvra e o valor é o TF
def TF_Dic(texto):
    # Se necessário pré-tratamento
    
    texto = texto.replace(",", "").replace(".", "").replace("(", "").replace(")", "")
    texto = texto.lower().split()
    
    TFDic = {} # cria um dicionário vazio
    for palavra in texto:
        if palavra in TFDic: # se a palavra já existir no dicionário, soma um no contador
            TFDic[palavra] += 1
        else:
            TFDic[palavra] = 1 # se ela não existir, acrescenta com o valor 1
    # Para calcular o TF          
    for palavra in TFDic:
        TFDic[palavra] = TFDic[palavra] / len(texto)
    return TFDic

# Para calcular o IDF de todo corpora:
def IDF_Dic(lista_dic): # Recebe uma lista com os dicionários de TF de cada documento
    countDic = {}
    for dic in lista_dic: # Para cada dicionário na lista
        for palavra, TF in dic.items(): # Para cada palavra neste dicionário
            if palavra in countDic: # Se a palavra já está no dicionário IDF, somar 1 no valor
                countDic[palavra] += 1
            else: # Se não, adicionar ela com valor 1
                countDic[palavra] = 1
    idfDic = {}
    for palavra in countDic:
        idfDic[palavra] = math.log(len(lista_dic)/countDic[palavra])
    return idfDic # Retorna dicionário com os valores de idf de todo vocabulário


# Função que calcula o TF*IDF 
def TF_IDF(tfDic, idfDic):
    tfidf = {}
    for palavra in tfDic:
        tfidf[palavra] = tfDic[palavra]*idfDic[palavra]
    return tfidf       


# Função que faz uma lista com os TF*IDF de cada texto
def TF_IDF_Dic(lista_strings):
    # Para gerar uma lista de dicionários com o valor de TF de cada texto
    lista_dic = []
    for texto in lista_strings:
        lista_dic.append(TF_Dic(texto))
    # Para gerar um dicionário com os valores de IDF
    idfDic = IDF_Dic(lista_dic)
    # Para gerar uma lista de dicionários com o TFIDF de cada documento
    lista_tfidf = []
    for dic in lista_dic:
        lista_tfidf.append(TF_IDF(dic, idfDic))
    return lista_tfidf    
