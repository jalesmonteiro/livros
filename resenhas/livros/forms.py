from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
import json

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LivroForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['tags_texto'].initial = ', '.join(self.instance.tags.values_list('nome', flat=True))

    tags_texto = forms.CharField(
        required=False,
        label="Tags",
        help_text="Digite e pressione Enter para adicionar uma tag.",
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'id_tags_texto'})
    )

    class Meta:
        model = Livro
        fields = ['titulo', 'autor', 'data_publicacao', 'sinopse', 'capa']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'autor': forms.TextInput(attrs={'class': 'form-control'}),
            'sinopse': forms.Textarea(attrs={'class': 'form-control'}),
            'capa': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'data_publicacao': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'},
                format='%Y-%m-%d'
            ),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        # Se for um novo livro com capa, precisamos salvar sem a capa primeiro para ter o ID
        capa = self.cleaned_data.get('capa')
        if not self.instance.pk and capa:
            # Salva sem a capa para gerar o ID
            livro = super().save(commit=False)
            livro.capa = None
            livro.save()
            # Agora atribui a capa e salva novamente
            livro.capa = capa
            livro.save()
        else:
            livro = super().save(commit=commit)

        # Processa as tags
        tags_texto = self.cleaned_data.get('tags_texto', '')
        if commit:
            livro.tags.clear()
            if tags_texto:
                try:
                    tags_data = json.loads(tags_texto)
                    nomes_tags = [tag['value'].strip() for tag in tags_data if tag['value'].strip()]
                except Exception:
                    nomes_tags = [t.strip() for t in tags_texto.split(',') if t.strip()]
                for nome in nomes_tags:
                    tag, _ = Tag.objects.get_or_create(nome=nome)
                    livro.tags.add(tag)
        return livro


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