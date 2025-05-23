from datetime import date
from django.test import TestCase
from django.urls import reverse
from livros.models import *

class PermissionTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='12345')
        self.user2 = User.objects.create_user(username='user2', password='12345')
        self.livro = Livro.objects.create(titulo="Livro Teste", autor="Autor", data_publicacao=date(2020, 1, 1))
        self.resenha = Resenha.objects.create(
            livro=self.livro,
            usuario=self.user1,
            texto="Resenha do User1",
            nota=4
        )

    def test_exclusao_resenha_apenas_autor(self):
        self.client.login(username='user2', password='12345')
        response = self.client.get(reverse('excluir_resenha', args=[self.resenha.id]))
        self.assertEqual(response.status_code, 403)  # Forbidden
