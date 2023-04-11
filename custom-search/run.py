from libs.engine import SearchEngine
import json
import os.path
import argparse
import validators
import requests
from tqdm import tqdm





def readProfile(_file):
    with open(_file,'r') as f:
        data = json.load(f)
    return data

def getQueries(_profile):
    data = {}
    
    
    if 'queries' in _profile and os.path.isfile(_profile['queries']):
        queries = []
        with open(_profile['queries']) as f:
            for i in f:
                i = i.replace('\n','').replace('\r','').replace('\t','')
                if i:
                    queries.append(i) 
            data['querys'] = queries
            return [data]
    else:
        #Check if is URL
        valid = validators.url(_profile['api-url'])
        if valid:
            r = requests.get(_profile['api-url']+'/get/all/job')
            jobs = r.json()
            if len(jobs) == 0:
                return None
            qAux = requests.get(_profile['api-url']+'/get/all/query').json()
            print(qAux)
            nulo = True
            if len(qAux) > 0:
                for query in qAux:                    
                    for job in jobs:
                        nulo = True
                        job['querys'] =  [a for a in job['querys'] if not query['query'] in job['querys']]
                        if job['querys']:
                            nulo = False
                if nulo:
                    return None
            
            return jobs

    return None

def getSaveQueryResult(_profile):
    # 0 - diretorio
    # 1 - api
    # None - invalido
    if 'result-path' in _profile:
        if os.path.isdir(_profile['result-path']):
            return 0
    else:
        #Check if is URL
        valid = validators.url(_profile['api-url']+'/insert/query')
        if valid:
            return 1

    return None

parser = argparse.ArgumentParser(description = 'Script to start scrapper.')
parser.add_argument('--profile', action = 'store', dest = 'profile', required = True, help = 'set profile file')
parser.add_argument('--TEST', action='store_true',  required = False, help = 'set test mode')

arguments = parser.parse_args()

# 1 - Ler o arquivo com o profile do scrapper
profile = readProfile(arguments.profile)
print(profile)

# 2 - Lendo/Recebendo as querys
data = getQueries(profile)
print(data)
if not data:
    print('Sem buscas para executar!')
    exit(0)

# 3 - Definindo local para armazernar os resultado
saveTo = getSaveQueryResult(profile)



for job in data:
    for query in job['querys']: 
        query = query.replace('\n','')
        print('Query:',query)
        resp = {}
        if(arguments.TEST):  
            #AMBIENTE PARA TESTE
            _f = query.replace(' ','-')+'.json'
            
            with open(profile['test-folder']+_f,'r') as f:
                resp = json.load(f)
        else:
            capes_engine = SearchEngine().capes(profile)
            result = capes_engine.search(query)
            resp = {'result':result,
            'query':query}    
            capes_engine.browser.quit()   

        if saveTo == 0:
            r_file = query.replace(' ','-')
            print('Salvando no diretório:',profile['result-path'])
            with open('{}/{}.json'.format(profile['result-path'],r_file),'w') as f:
                json.dump(resp,f,indent=4, sort_keys=True)
        elif saveTo == 1:
            print('Salvando na API:',profile['result-path'])
            IDs = {}
            for i,article in enumerate(tqdm(resp['result'])):
                # resp['result'][i]['_id'] = 0
                r = requests.post(profile['result-path'],json=article)
                if '_id' in r.json():
                    IDs[i] = r.json()['_id']
                    resp['result'][i]['_id'] = r.json()['_id']
            
            #Atrelando os IDs dos artigos na query
            articles =  [ (i['_id'],None,None) for i in  resp['result']]
            query_data = {
                'query':query,
                'state' : 'Done',
                'userId' : job['user'],
                'jobId': job['_id'],
                'articles' : articles,
                'used': True,
            }

            r = requests.post(profile['api-url']+'/insert/query',json=query_data)
            if '_id' in r.json():
                print(r.json()['_id'])



   
