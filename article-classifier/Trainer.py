from core.Classifier import Classifier
from core.Model import Model
import xlrd
import scipy
import joblib
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, precision_score,pairwise_distances, accuracy_score, f1_score
from sklearn.model_selection import StratifiedKFold
from tqdm import tqdm
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import operator
import rank_bm25
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import random
import csv
import sys
import os
from joblib import Parallel, delayed
import datetime
import json
from core.Util import *
import requests


_path = '../models-article-classifier'
now = datetime.datetime.now().strftime('%d-%m-%Y')



tqdm_disable = True

args = {}

N_CORES = 32
FEATURE = 'abstract'
METRIC = accuracy_score


ip_backend = 'http://192.168.10.34:8000'


print('Pegando lista de Jobs!')
r = requests.get(ip_backend+'/api/get/all/job')
jobs_list = r.json()
for job in jobs_list:
    print(job['_id'])


    # for file_query in args['list']:
    print('Lendo JSON de entrada!')
    # data = []
    # # with open(file_query) as f:
    # with open(args['list'][0]) as f:
    #     data = json.load(f)


    
    r = requests.get(ip_backend+'/api/get/all/query')
    aux = r.json()
    querys = [ a for a in aux if a['jobId'] == job['_id']]


    #Recuperando os artigos
    ids = {}
    for query in querys:
        for article in query['articles']:
            if not article[0] in ids:
                _id = article[0]
                r = requests.get(ip_backend+'/api/get/one/article',json={'_id':_id}).json()
                if len(r)>0:
                    r['relevant'] = article[1] 
                    r['preditc'] = article[2]
                    ids[_id] = r
        query['articles'] = [ids[i] for i in ids]
        

        
    data = []


    for _j, query in enumerate(querys):
        print(query['query'])
        if not query['articles']:
            continue

        _pop = []
        for i in range(len(query['articles'])):
            if not query['articles'][i][FEATURE]:
                _pop.append(i)

        _pop.reverse()
        for i in _pop:
            del query['articles'][i]




        print('Analisando a lingua dos textos!')
        MAX = len(query['articles'])
        aux = Parallel(n_jobs=N_CORES)(delayed(analiser)(query['articles'][i][FEATURE]) for i in tqdm(range(MAX),file=sys.stdout,disable=tqdm_disable))

        t = []
        for i in range(len(query['articles'])):    
            if aux[i]:
                query['articles'][i]['lang'] = [aux[i][0]]
            else:
                t.append(i)
        t.reverse()
        for i in t:
            del query['articles'][i]

        print('Tokenizando os textos!')
        MAX = len(query['articles'])
        t = []
        aux = Parallel(n_jobs=N_CORES)(delayed(filtering)(query['articles'][i][FEATURE],query['articles'][i]['lang']) for i in tqdm(range(MAX),file=sys.stdout,disable=tqdm_disable))
        for i in range(len(query['articles'])):  
            query['articles'][i]['words'] = aux[i]
            if not aux[i]:
                t.append(i)
        t.reverse()
        for i in t:
            del query['articles'][i]

        print('Contando os tokens!')
        MAX = len(query['articles'])
        aux = Parallel(n_jobs=N_CORES)(delayed(TextCounter)(query['articles'][i][FEATURE]) for i in tqdm(range(MAX),file=sys.stdout,disable=tqdm_disable))
        aux = [ TextCounter(query['articles'][i]['words']) for i in tqdm(range(MAX),file=sys.stdout,disable=tqdm_disable) ]
        for i in range(len(query['articles'])):    
            query['articles'][i]['words'] = aux[i]
            data.append(query['articles'][i])
            
            
            
            
    #CRIANDO O DICIONARIO
    dicinario = {}
    _id = 0
    print('Criando o dicionário de palavras!')
    for i in tqdm(data):
        for word in i['words']:
            if word in dicinario:
                dicinario[word]['value'] += i['words'][word]
            else:
                dicinario[word] = {
                    'value': i['words'][word],
                    'id':_id
                }
                _id +=1


    # #Processando a query
    # q_aux = TextCounter(data['resume-query']) 
    # for word in q_aux:
    #     if word in dicinario:
    #         dicinario[word]['value'] += q_aux[word]
    #     else:
    #         dicinario[word] = {
    #             'value': q_aux[word],
    #             'id':_id
    #         }
    #         _id +=1

    # q_vet = Vectorize(dicinario,[q_aux])
    # q_sparse = scipy.sparse.csr_matrix(q_vet)[0]


    # print(data[0])


    texts = [i['words'] for i in data]
    labels = []
    label_map = {}
    c_label = 0
    for i in data:
    #     if i['relevant']:
    #         print(i)
    # #     if not 'relevant' in i:
    #         i['relevant'] = False
        if not i['relevant'] in label_map:
            label_map[i['relevant']] = c_label
            c_label += 1
        labels.append(label_map[i['relevant']])
    print(label_map)  



    #TODO: MELHORAR A VETORIZAÇÃO PARA O MODELO CSR
    vets = Vectorize(dicinario,texts)
    vets_sparse = scipy.sparse.csr_matrix(vets)

    #Separando teste e treino balanceados
    seed = 2019
    nFold = 10
    skf = StratifiedKFold(n_splits=nFold,random_state=seed,shuffle=True)
    cont=1

    folds = {}
    for train_index,test_index in skf.split(texts,labels):
        TRAIN = [vets[i] for i in train_index]
        TRAIN =  scipy.sparse.csr_matrix(TRAIN)
        LABELS = [labels[i] for i in train_index]    
        TEST = [vets[i] for i in test_index]
        TEST =  scipy.sparse.csr_matrix(TEST)
        y_true = [labels[i] for i in test_index]
        folds[cont]={
            'train': TRAIN,
            'labels': LABELS,
            'test':TEST,
            'y_true':y_true
        }
        cont+=1    



    models = {}
    result = []
    n_runs = 10

    print('KNN train!')
    MAX = nFold*n_runs
    with tqdm(total=MAX,file=sys.stdout,disable=tqdm_disable) as pbar:
        for r in range(n_runs):
            seed = round(random.random()*1000)
            classificador = Classifier()
            classificador.setAlgorithm('knn')
            # classificador.algorithm.set_params(**{'random_state':seed})
            accs = []
            for fold in folds:
                y_pred = []            
                classificador.trainModel(folds[fold]['train'],folds[fold]['labels'])
                for test in folds[fold]['test']:        
                    y_pred.append(classificador.algorithm.predict(test))
                accs.append(METRIC(folds[fold]['y_true'],y_pred))
                pbar.update(1)
            acc = np.mean(accs)
            run = '{}-{}'.format('knn',seed)
            models[run] = classificador
            result.append((run,acc))

    result_sort = sorted(result, key=lambda tup: tup[1],reverse=True)
    sort_n = 3
    MAX = len(vets)
    n_result = []

    print('Selecionando os {} melhores modelos para retreinar com todos os dados e avalaiar com todos'.format(sort_n))
    for i in result_sort[:sort_n]:
        model = i[0]
        m_acc = i[1]
    #         print(model,m_acc)
        models[model].trainModel(vets_sparse,labels)
        y_pred = []
        with tqdm(total=MAX,file=sys.stdout,disable=tqdm_disable) as pbar:
            for test in vets_sparse:
                y_pred.append(models[model].algorithm.predict(test))
                pbar.update(1)
        n_acc = METRIC(labels,y_pred)
    #         print('Accuracy:',n_acc)
    #         print(confusion_matrix(labels,y_pred))
    #         print('------------------')
        n_result.append((model,n_acc))


    print('RandomForest train!')
    MAX = nFold*n_runs
    with tqdm(total=MAX,file=sys.stdout,disable=tqdm_disable) as pbar:
        for r in range(n_runs):
            seed = round(random.random()*1000)
            classificador = Classifier()
            classificador.setAlgorithm('randomForest')
            # classificador.algorithm.set_params(**{'random_state':seed})
            accs = []
            for fold in folds:
                y_pred = []            
                classificador.trainModel(folds[fold]['train'],folds[fold]['labels'])
                for test in folds[fold]['test']:        
                    y_pred.append(classificador.algorithm.predict(test))
                accs.append(METRIC(folds[fold]['y_true'],y_pred))
                pbar.update(1)
            acc = np.mean(accs)
            run = '{}-{}'.format('randomForest',seed)
            models[run] = classificador
            result.append((run,acc))

    result_sort = sorted(result, key=lambda tup: tup[1],reverse=True)
    sort_n = 3
    MAX = len(vets)
    n_result = []

    print('Selecionando os {} melhores modelos para retreinar com todos os dados e avalaiar com todos'.format(sort_n))
    for i in result_sort[:sort_n]:
        model = i[0]
        m_acc = i[1]
        print(model,m_acc)
        models[model].trainModel(vets_sparse,labels)
        y_pred = []
        with tqdm(total=MAX,file=sys.stdout,disable=tqdm_disable) as pbar:
            for test in vets_sparse:
                y_pred.append(models[model].algorithm.predict(test))
                pbar.update(1)
        n_acc = METRIC(labels,y_pred)
        print('Accuracy:',n_acc)
        print(confusion_matrix(labels,y_pred))
    #         print('------------------')
        n_result.append((model,n_acc))

    result_sort = sorted(n_result, key=lambda tup: tup[1],reverse=True)

    print('Salvando o melhor modelo')
    model = result_sort[0][0]
    acc = result_sort[0][1]
    bModel = Model(_classifier=models[model],_dictionary=dicinario,_features=vets,_labels=labels,_seed=seed,_acc=acc,_label_map=label_map)
    bModel.saveModel(_output='model-'+job['_id']+'.joblib')



