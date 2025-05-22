from django.db import models
from django.contrib.auth.models import User
import random

def gerar_cor_hex():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

class Tag(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    cor = models.CharField(max_length=7, default=gerar_cor_hex, editable=False)

    def __str__(self):
        return self.nome

class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    data_publicacao = models.DateField()
    sinopse = models.TextField(blank=True)
    capa = models.ImageField(upload_to='capas/', blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='livros')

    def __str__(self):
        return f"{self.titulo} ({self.autor})"

    @property
    def lista_tags(self):
        # Retorna uma lista com os nomes das tags associadas ao livro
        return list(self.tags.values_list('nome', flat=True))

    def media_avaliacoes(self):
        avaliacoes = self.resenhas.all()
        if avaliacoes:
            return round(sum([r.nota for r in avaliacoes]) / len(avaliacoes), 2)
        return None

class Resenha(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, related_name='resenhas')
    texto = models.TextField()
    nota = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    data_publicacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resenha de {self.livro} por {self.usuario.username}"