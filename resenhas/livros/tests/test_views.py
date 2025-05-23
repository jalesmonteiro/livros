from datetime import date
from django.test import Client, TestCase
from django.urls import reverse
from livros.models import *

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.livro = Livro.objects.create(titulo="O Alienista", autor="Machado de Assis", data_publicacao=date(2020, 1, 1))

    # --- Testes de Acesso ---
    def test_home_redirect_se_nao_autenticado(self):
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('home'))

    def test_adicionar_livro_autenticado(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('adicionar_livro'))
        self.assertEqual(response.status_code, 200)

    # --- Testes de Funcionalidade ---
    def test_busca_livros(self):
        self.client.login(username='testuser', password='12345')  # Faça login antes!
        response = self.client.get(reverse('buscar_livros') + '?q=Alienista')
        self.assertContains(response, "O Alienista")

    def test_paginacao_listar_livros(self):
        self.client.login(username='testuser', password='12345')  # Faça login antes!
        # Cria 25 livros para testar paginação
        for i in range(25):
            Livro.objects.create(titulo=f"Livro {i}", autor="Autor", data_publicacao=date(2020, 1, 1))
        response = self.client.get(reverse('listar_livros') + '?quantidade=8&page=2')
        self.assertEqual(len(response.context['page_obj']), 8)
