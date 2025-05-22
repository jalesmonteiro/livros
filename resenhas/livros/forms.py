from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = ['titulo', 'autor', 'data_publicacao', 'sinopse', 'capa']
        widgets = {
            'data_publicacao': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'},
                format='%Y-%m-%d'
            ),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

class ResenhaForm(forms.ModelForm):
    class Meta:
        model = Resenha
        fields = ['texto', 'nota']
        widgets = {
            'texto': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'nota': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'texto': 'Sua resenha',
            'nota': 'Nota',
        }