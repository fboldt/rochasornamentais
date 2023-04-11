from django.forms import ModelForm
from django import forms
from .models import UserDefault

class UserForm(forms.ModelForm):
	class Meta:
		
		model = UserDefault
		fields = ('username', 'password', )
		
		widgets = {
			'username': forms.TextInput(attrs = {
                'placeholder':'Usuário',
                'name':'username',
                'id':'username',
                'maxlength': 200
            }),
            'password': forms.PasswordInput(attrs = {
                'placeholder':'Senha',
                'name':'password',
                'id':'password',
                'maxlength': 200
            }),
		}
