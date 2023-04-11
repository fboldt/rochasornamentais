import json
import requests




print('Teste: Enviando um artigo para o banco!')
URL = 'http://localhost:8080/api/article/'
data = ''
with open('/dados/resultados-buscas/ornamental-stone-processing-waste-recycling.json') as f:
    data = json.load(f)


for article in data:
    d = {
        'title' : article['title'],
        'authors' : article['author'],
        'abstract':article['abstract'],
        'year':2020,
        'link':URL,
        'filde_doc':'Null'
    }
    F = {'file' : open('teste.pdf','rb')}
    r = requests.post(URL,data=d,files=F)
