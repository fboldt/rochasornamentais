import argparse
import joblib
import json
from core.Model import Model
import os
from sklearn.metrics import accuracy_score
from joblib import Parallel, delayed
from tqdm import tqdm
import csv
from core.Util import *
import requests

ap = argparse.ArgumentParser()
ap.add_argument('-m','--model',required=False,help='File of model in joblib.')
# ap.add_argument('-l','--list',required=True,help='List of texts for inference.')
ap.add_argument('-a','--algorithm',required=False,
help='Set wich algorithm is the model.')
ap.add_argument('-d','--dictionary',required=False,
help='Set dictionary.')

args = vars(ap.parse_args())

N_JOBS = 32
FEATURE = 'abstract'
METRIC = accuracy_score
ip_backend = 'http://192.168.10.34:8000'



print('Pegando lista de Jobs!')
r = requests.get(ip_backend+'/api/get/all/job')
jobs_list = r.json()
for job in jobs_list:
    print(job['_id'])


    r = requests.get(ip_backend+'/api/get/all/query')
    aux = r.json()
    querys = [ a for a in aux if a['jobId'] == job['_id']]


    #Recuperando os artigos
    ids = {}
    documents = []
    for query in querys:
        for article in query['articles']:
            if not article[0] in ids:
                _id = article[0]
                r = requests.get(ip_backend+'/api/get/one/article',json={'_id':_id}).json()
                if len(r)>0:
                    r['relevant'] = article[1] 
                    r['predict'] = article[2]
                    ids[_id] = r
        aux = []
        for i in ids:
            if ids[i][FEATURE]  is None:
                ids[i]['predict'] = -1
                
            if ids[i]['relevant'] is None:
                aux.append(ids[i])
        # aux = [ids[i] for i in ids if ids[i][FEATURE] is not None]
        aux = [i for i in aux if i['predict'] != -1]
        documents.extend(aux)


    # exit(0)
    # r = requests.get(ip_backend+'/api/get/all/query')
    # resp = r.json()
    # documents = []
    # for i in resp:
    #     if i['articles']:
    #         for j in i['articles']:
    #             if j[FEATURE]:
    #                 if not 'relevant' in  j:
    #                     j['relevant'] =  False
    #                 documents.append(j)


    # exit(0)
            

    #CARREGANDO O MODELO
    print('Loading model!')
    model = Model()
    model.loadModel('model-'+job['_id']+'.joblib')
    print('Model Accuracy:',model.acc)


    MAX = len(documents)
    # print(documents[0]['articles'])
    # for i in documents:
    #     analiser(i['articles'][FEATURE])
    # #     print(i['articles'])
    aux = Parallel(n_jobs=N_JOBS)(delayed(analiser)(documents[i][FEATURE]) for i in tqdm(range(MAX)))

    t = []
    for i in range(len(documents)):    
        if aux[i]:
            documents[i]['lang'] = [aux[i][0]]
        else:
            t.append(i)

    t.reverse()
    print('Removendo os items que a lingua não possuimos modelos!')
    for i in t:
        del documents[i]

    MAX = len(documents)
    t = []
    aux = Parallel(n_jobs=N_JOBS)(delayed(filtering)(documents[i][FEATURE],documents[i]['lang']) for i in tqdm(range(MAX)))
    for i in range(len(documents)):  
        documents[i]['text'] = aux[i]
        if not aux[i]:
            t.append(i)

    t.reverse()
    print('Removendo os items que não geram textos tokenizados!')
    for i in t:
        del documents[i]

    MAX = len(documents)

    aux = Parallel(n_jobs=N_JOBS)(delayed(TextCounter)(documents[i]['text']) for i in tqdm(range(MAX)))
    for i in range(len(documents)):    
        documents[i]['words'] = aux[i]

    texts = [i['words'] for i in documents]
    labels = []
    for i in documents:
        labels.append(model.label_map[i['relevant']])

    vets = Vectorize(model.dictionary,texts)


    y_pred = []
    for i in vets:
        _id = model.classifier.algorithm.predict([i])[0]
        y_pred.append(_id)
        for label, val in model.label_map.items():
            if val == _id:
                print(label)
    print('Accuracy: ',accuracy_score(labels,y_pred))
