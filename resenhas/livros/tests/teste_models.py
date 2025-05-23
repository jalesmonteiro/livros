from datetime import date
from django.contrib.auth.models import User
from django.test import TestCase
from livros.models import Livro, Resenha, Tag

class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.livro = Livro.objects.create(
            titulo="Dom Casmurro",
            autor="Machado de Assis",
            data_publicacao=date(1899, 1, 1)
        )
        self.resenha = Resenha.objects.create(
            livro=self.livro,
            usuario=self.user,
            texto="Uma obra-prima!",
            nota=5
        )

    def test_criacao_livro(self):
        self.assertEqual(self.livro.titulo, "Dom Casmurro")
        self.assertEqual(str(self.livro), "Dom Casmurro (Machado de Assis)")

    def test_media_avaliacoes(self):
        self.assertEqual(self.livro.media_avaliacoes(), 5.0)
        Resenha.objects.create(livro=self.livro, usuario=self.user, texto="Bom", nota=3)
        self.assertEqual(self.livro.media_avaliacoes(), 4.0)

    def test_lista_tags(self):
        tag = Tag.objects.create(nome="Clássico")
        self.livro.tags.add(tag)
        self.assertEqual(self.livro.lista_tags, ["Clássico"])
