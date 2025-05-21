from django.db import models
from django.contrib.auth.models import User

class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    data_publicacao = models.DateField()
    sinopse = models.TextField(blank=True)
    capa = models.ImageField(upload_to='capas/', blank=True, null=True)

    def __str__(self):
        return f"{self.titulo} ({self.autor})"

    def media_avaliacoes(self):
        avaliacoes = self.resenha_set.all()
        if avaliacoes:
            return round(sum([r.nota for r in avaliacoes]) / len(avaliacoes), 2)
        return None

class Resenha(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    texto = models.TextField()
    nota = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    data_publicacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resenha de {self.livro} por {self.usuario.username}"
