import json


profile = {}
profile['institute'] = input('Instiuição UFES ou IFES: ')
if profile['institute'] == 'UFES':
    profile['institute'] = 'UFES - UNIVERSIDADE FEDERAL DO ESPÍRITO SANTO'
elif profile['institute'] == 'IFES':
    profile['institute'] = 'IFES - INSTITUTO FEDERAL DO ESPÍRITO SANTO'
else:
    print('Instituição não cadastrada!')
    exit(0)
profile['username'] = input('Usuário: ')
profile['password'] = input('Senha: ')
profile['download-path'] = input('Camiho para armazenar os artigos baixados: ')
profile['result-path'] = input('Camiho para armazenar os metadados dos artigos: ')
profile['queries'] = input('Arquivo ou URL do banco de queries: ')
profile['max-pages'] = input('Quantidade máxima de páginas buscadas, -1 para todas: ')


print('Salvando o arquivo de profile!')
with open('profile.json','w') as f:
    json.dump(profile,f,indent=4)        