from datetime import date
from django.test import TestCase
from django.urls import reverse
from livros.models import *

class PermissionViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.livro = Livro.objects.create(
            titulo="Dom Casmurro",
            autor="Machado de Assis",
            data_publicacao=date(1899, 1, 1)
        )
        self.resenha = Resenha.objects.create(
            usuario=self.user,
            livro=self.livro,
            texto="Ótima leitura!",
            nota=5
        )
    
    def assertLoginRedirect(self, url, method='get', data=None):
        if method == 'post':
            response = self.client.post(url, data or {})
        else:
            response = self.client.get(url)
        login_url = reverse('login')
        self.assertRedirects(response, f'{login_url}?next={url}')

    def test_home_requer_login(self):
        self.assertLoginRedirect(reverse('home'))

    def test_listar_livros_requer_login(self):
        self.assertLoginRedirect(reverse('listar_livros'))

    def test_detalhe_livro_requer_login(self):
        self.assertLoginRedirect(reverse('detalhe_livro', args=[self.livro.id]))

    def test_adicionar_livro_requer_login(self):
        self.assertLoginRedirect(reverse('adicionar_livro'))

    def test_buscar_livros_requer_login(self):
        self.assertLoginRedirect(reverse('buscar_livros'))

    def test_editar_livro_requer_login(self):
        self.assertLoginRedirect(reverse('editar_livro', args=[self.livro.id]))

    def test_excluir_livro_requer_login(self):
        self.assertLoginRedirect(reverse('excluir_livro', args=[self.livro.id]))

    def test_adicionar_resenha_requer_login(self):
        self.assertLoginRedirect(reverse('adicionar_resenha', args=[self.livro.id]))

    def test_excluir_resenha_requer_login(self):
        self.assertLoginRedirect(reverse('excluir_resenha', args=[self.resenha.id]))

    # Exemplo de POST protegido
    def test_excluir_livro_post_requer_login(self):
        self.assertLoginRedirect(reverse('excluir_livro', args=[self.livro.id]), method='post')

    def test_excluir_resenha_post_requer_login(self):
        self.assertLoginRedirect(reverse('excluir_resenha', args=[self.resenha.id]), method='post')

