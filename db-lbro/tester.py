import json
import requests


print('SCRIPT DE TESTE DA API')



# print('Teste: Enviando um artigo para o banco!')
# URL = 'http://localhost:8080/api/article/'
# data = ''
# with open('teste-1.json') as f:
#     data = json.load(f)

# F = {'file' : open('teste.pdf','rb')}
# r = requests.post(URL,data=data,files=F)
# print(r.text)


print('Teste: Criando uma query!')
URL = 'http://localhost:8080/api/query/'
data = ''
with open('teste-2.json') as f:
    data = json.load(f)
r = requests.post(URL,data=data)
print(r.text)

print('-------------------------------------')
print('Teste: Recuperando query!')
URL = 'http://localhost:8080/api/query/'
data = ''
with open('teste-2.json') as f:
    data = json.load(f)
r = requests.get(URL,params=data)
print(r.text)