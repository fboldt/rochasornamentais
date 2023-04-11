import json
from django.http import JsonResponse
# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate
# from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.csrf import csrf_protect
from django.core import serializers
import time

# from rest_framework import generics
# from rest_framework.response import Response
# from rest_framework.authtoken.models import Token
# from rest_framework.authentication import SessionAuthentication
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
# from rest_framework.decorators import api_view, permission_classes, renderer_classes
# from rest_framework.status import (
#     HTTP_400_BAD_REQUEST,
#     HTTP_404_NOT_FOUND,
#     HTTP_200_OK
# )

from . import models
# from . import form
from . import utils
from app.form import *

def article(request):
    if request.method == 'POST':
        #TODO:ASSUMINDO QUE SERÁ PELO JSON
        form = ArticleForm(request.POST)
        if form.is_valid():
            print('Formulário valido')
            print(str(form.cleaned_data))
            t = models.Article.objects.filter(title=form.data['title'])
            f = request.FILES['file'].read()
            print(t.exists())
            if not t.exists():
                docID = utils.saveFile(f)
                print(docID)
                instace = form.save(commit=False)
                instace.file_doc = docID                
                instace.save()
            return JsonResponse({'status' : True})
        else:
            print('Formulário invalido')
            return JsonResponse({'status' : False})



from django.core import serializers

def query(request):
    # Retornar a 
    if request.method == 'GET':
        form = GetQueryForm(request.GET)
        if form.is_valid():
            print('Formulário valido')
            query = models.Query.objects.get(query=form.data['query'],user=form.data['user'])
            response = serializers.serialize('json',[query])
            response = json.loads(response)[0]['fields']
        return JsonResponse({'status' : True,'response':response})

    elif request.method == 'POST':
        form = InsertQueryForm(request.POST)        
        if form.is_valid():
            print('Formulário valido')
            now = str(time.time())
            t = models.Query.objects.filter(query=form.data['query'],user=form.data['user'])
            # Check if querys as inserted
            if not t.exists():
                instance  =  form.save(commit=False)
                instance.date = now
                instance.save()
            return JsonResponse({'status' : True})
        else:
            return JsonResponse({'status' : False})


def list_queries(request):
    # Return lis of queries
    if request.method == 'GET':
        all_queries = models.Query.objects.all()
        all_queries = serializers.serialize('json',all_queries)
        all_queries = json.loads(all_queries)
        response = []
        for query in all_queries:
            response.append(query['fields'])
        return JsonResponse({'status' : True, 'response':response})
    else:
        return JsonResponse({'status' : False})




    