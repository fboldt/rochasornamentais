from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from core.Model import Model
from core.Classifier import Classifier
import core.Util
import json
import joblib
import os
from sklearn.ensemble import RandomForestClassifier


CURRENT_DIR = os.path.dirname(__file__)
a = joblib.load('/dados/models-article-classifier/model-12-02-2020-0.99831.joblib')

@csrf_exempt
def home(request):
    return JsonResponse({
        'message': 'Hello World!',
        'status' : True
    })



@csrf_exempt
def inference(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        received_json_data = json.loads(data)
        print(received_json_data)
        if received_json_data['text']:
            #Carregando o modelo
            # except ModuleNotFoundError:
                # pass
            #Processando o texto
            text = {'text': received_json_data['text']}
            text['lang'] = core.Util.analiser(text['text'])
            text['content'] = core.Util.filtering(text['text'],text['lang'])
            text['words'] = core.Util.TextCounter(text['content'])
            vets = core.Util.Vectorize(a.dictionary,[text['words']])
            resp = False
            for i in vets:
                _id = a.classifier.algorithm.predict([i])[0]
                for label, val in a.label_map.items():
                    if val == _id:
                        resp = True
            return JsonResponse({'status':True,
            'label': resp
            })



