from django.forms import ModelForm
from . import models
from django import forms


class ArticleForm(ModelForm):
    class Meta:
        model = models.Article
        fields = '__all__'

class InsertQueryForm(ModelForm):
    class Meta:
        model =  models.Query
        fields = ['query','user']


class GetQueryForm(forms.Form):
    class Meta:
        model =  models.Query
        fields = ['query','user']
