import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from .models import Query, Article, UserDefault
from .serializers import QuerySerializer, ArticleSerializer, UserDefaultSerializer
from .enginesearch import start
from .forms import UserForm
from .utils import encrypt
from .enginesearch.libs.database.database import Connection

def index(request):
    return render(request, 'index.html', {})

def api_search(request):
    try:
        body = request.body.decode('utf-8')
        obj_body = json.loads(body)
        start(obj_body)
    except Exception as exc:
        print(exc)
        return False
    return render(request, 'index.html', {})

def api_login(request):
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        obj_body = json.loads(body)
        get = Connection().get_user(obj_body['email'], obj_body['password'])
        response = { 
            'validation': True, 
            'method': 'login' 
            } if get['errors'] == '' else { 
            'validation': False, 
            'method': 'login',
            'errors': get['errors'] 
        }
        return JsonResponse(response)

def api_register(request):
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        obj_body = json.loads(body)
        insert = Connection().insert_user(obj_body)
        response = { 
            'validation': True, 
            'method': 'register' 
            } if insert['errors'] == '' else { 
            'validation': False, 
            'method': 'register',
            'errors': insert['errors'] 
        }
        return JsonResponse(response)

def api_users(request):
    if request.method == 'POST':
        return JsonResponse(Connection().all_users())

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html', {})

def register(request):
    if request.method == 'GET':
        return render(request, 'register.html', {})

def delete_query(request):
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        obj_body = json.loads(body)
        deleted = Connection().delete_query(obj_body)
        response = {
            'validation': deleted
        }
        return JsonResponse(response)

def test(request):
    response = Response(
        { 'sample_data': 123 }, 
        status=HTTP_200_OK
    )
    response.accepted_renderer = JSONRenderer()
    response.accepted_media_type = "application/json"
    response.renderer_context = {}

    return response

class QueryList(generics.ListCreateAPIView):
    queryset = Query.objects.all()
    serializer_class = QuerySerializer

class ArticleList(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class UserList(generics.ListCreateAPIView):
    queryset = UserDefault.objects.all()
    serializer_class = UserDefaultSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = (IsAuthenticated, )
