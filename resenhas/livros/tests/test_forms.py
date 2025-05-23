from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from livros.forms import *
from PIL import Image
from datetime import date
from django.test import TestCase, override_settings
from django.conf import settings
import shutil
import tempfile
import io

class RegistroFormTests(TestCase):
    def test_form_valido(self):
        """Formulário válido com todos os campos corretos."""
        form_data = {
            'username': 'novousuario',
            'email': 'novo@email.com',
            'password1': 'SenhaForte123!',
            'password2': 'SenhaForte123!',
        }
        form = RegistroForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalido_senhas_diferentes(self):
        """Formulário inválido se as senhas não coincidirem."""
        form_data = {
            'username': 'novousuario',
            'email': 'novo@email.com',
            'password1': 'SenhaForte123!',
            'password2': 'OutraSenha123!',
        }
        form = RegistroForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_form_invalido_email_faltando(self):
        """Formulário inválido se o email não for informado."""
        form_data = {
            'username': 'novousuario',
            'email': '',
            'password1': 'SenhaForte123!',
            'password2': 'SenhaForte123!',
        }
        form = RegistroForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_form_invalido_username_existente(self):
        """Formulário inválido se o username já existir."""
        User.objects.create_user(username='novousuario', email='existe@email.com', password='senhaqualquer')
        form_data = {
            'username': 'novousuario',
            'email': 'novo@email.com',
            'password1': 'SenhaForte123!',
            'password2': 'SenhaForte123!',
        }
        form = RegistroForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_form_invalido_email_invalido(self):
        """Formulário inválido se o email for inválido."""
        form_data = {
            'username': 'novousuario',
            'email': 'naoeumemail',
            'password1': 'SenhaForte123!',
            'password2': 'SenhaForte123!',
        }
        form = RegistroForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class LivroFormTests(TestCase):
    def setUp(self):
        self.tag1 = Tag.objects.create(nome="Ficção")
        self.tag2 = Tag.objects.create(nome="Clássico")

    def test_form_valido_campos_obrigatorios(self):
        """Formulário válido com campos obrigatórios preenchidos."""
        form_data = {
            'titulo': 'Dom Casmurro',
            'autor': 'Machado de Assis',
            'data_publicacao': '1899-01-01',
            'sinopse': 'Um clássico da literatura brasileira.',
            'tags_texto': '[{"value":"Ficção"},{"value":"Clássico"}]'
        }
        form = LivroForm(data=form_data)
        self.assertTrue(form.is_valid())
        livro = form.save()
        self.assertEqual(livro.titulo, 'Dom Casmurro')
        self.assertEqual(list(livro.tags.all()), [self.tag1, self.tag2])

    def test_form_valido_sem_sinopse_e_capa(self):
        """Formulário válido mesmo que sinopse e capa estejam em branco."""
        form_data = {
            'titulo': 'Livro Sem Sinopse',
            'autor': 'Autor',
            'data_publicacao': '2000-01-01',
            'sinopse': '',
            'tags': []
        }
        form = LivroForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalido_sem_titulo(self):
        """Formulário inválido se título faltar."""
        form_data = {
            'titulo': '',
            'autor': 'Autor',
            'data_publicacao': '2000-01-01',
            'sinopse': 'Qualquer coisa',
            'tags': []
        }
        form = LivroForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('titulo', form.errors)

    def test_form_invalido_sem_autor(self):
        """Formulário inválido se autor faltar."""
        form_data = {
            'titulo': 'Livro',
            'autor': '',
            'data_publicacao': '2000-01-01',
            'sinopse': '',
            'tags': []
        }
        form = LivroForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('autor', form.errors)

    def test_form_invalido_sem_data_publicacao(self):
        """Formulário inválido se data_publicacao faltar."""
        form_data = {
            'titulo': 'Livro',
            'autor': 'Autor',
            'sinopse': '',
            'tags': []
        }
        form = LivroForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('data_publicacao', form.errors)

    def test_form_invalido_data_publicacao_invalida(self):
        """Formulário inválido se data_publicacao for inválida."""
        form_data = {
            'titulo': 'Livro',
            'autor': 'Autor',
            'data_publicacao': 'dataerrada',
            'sinopse': '',
            'tags': []
        }
        form = LivroForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('data_publicacao', form.errors)

    def test_form_valido_com_capa(self):
        """Formulário válido ao enviar uma capa (simulada)."""
        # Cria uma imagem JPEG em memória (não depende de arquivo externo)
        image_io = io.BytesIO()
        image = Image.new("RGB", (100, 100), color="red")
        image.save(image_io, format="JPEG")
        image_io.seek(0)

        capa_simulada = SimpleUploadedFile("capa.jpg", image_io.read(), content_type="image/jpeg")
        form_data = {
            'titulo': 'Livro com Capa',
            'autor': 'Autor',
            'data_publicacao': '2022-01-01',
            'sinopse': 'Tem capa!',
            'tags_texto': '[{"value":"Ficção"},{"value":"Clássico"}]'
        }
        form = LivroForm(data=form_data, files={'capa': capa_simulada})
        self.assertTrue(form.is_valid(), form.errors)
        livro = form.save()
        # O nome do arquivo deve conter o padrão 'livro_<id>.jpg'
        self.assertIn("livro_", livro.capa.name)
        self.assertTrue(livro.capa.name.endswith(".jpg"))

    def test_form_valido_tags_opcionais(self):
        """Formulário válido mesmo sem nenhuma tag."""
        form_data = {
            'titulo': 'Livro Sem Tag',
            'autor': 'Autor',
            'data_publicacao': '2022-01-01',
            'sinopse': '',
            'tags': []
        }
        form = LivroForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    @classmethod
    def tearDownClass(cls):
        # Remove o diretório temporário e todos os arquivos após os testes
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

class ResenhaFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.livro = Livro.objects.create(
            titulo="Dom Casmurro",
            autor="Machado de Assis",
            data_publicacao=date(1899, 1, 1)
        )

    def test_form_valido(self):
        """Formulário válido com texto e nota dentro do permitido."""
        form_data = {
            'texto': 'Excelente leitura!',
            'nota': 5
        }
        form = ResenhaForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalido_sem_texto(self):
        """Formulário inválido se o texto estiver vazio."""
        form_data = {
            'texto': '',
            'nota': 4
        }
        form = ResenhaForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('texto', form.errors)

    def test_form_invalido_sem_nota(self):
        """Formulário inválido se a nota não for informada."""
        form_data = {
            'texto': 'Gostei do livro!',
            # 'nota' não fornecida
        }
        form = ResenhaForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('nota', form.errors)

    def test_form_invalido_nota_abaixo_limite(self):
        """Formulário inválido se a nota for menor que 1."""
        form_data = {
            'texto': 'Não gostei.',
            'nota': 0
        }
        form = ResenhaForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('nota', form.errors)

    def test_form_invalido_nota_acima_limite(self):
        """Formulário inválido se a nota for maior que 5."""
        form_data = {
            'texto': 'Muito bom!',
            'nota': 6
        }
        form = ResenhaForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('nota', form.errors)

    def test_form_valido_nota_minima_maxima(self):
        """Formulário válido para nota mínima e máxima."""
        for nota in [1, 5]:
            form_data = {
                'texto': f'Resenha nota {nota}',
                'nota': nota
            }
            form = ResenhaForm(data=form_data)
            self.assertTrue(form.is_valid())

    def test_form_salva_resenha(self):
        """Testa se o formulário salva corretamente uma resenha."""
        form_data = {
            'texto': 'Obra marcante.',
            'nota': 4
        }
        form = ResenhaForm(data=form_data)
        self.assertTrue(form.is_valid())
        # Salva a resenha, associando manualmente usuário e livro
        resenha = form.save(commit=False)
        resenha.usuario = self.user
        resenha.livro = self.livro
        resenha.save()
        self.assertEqual(resenha.texto, 'Obra marcante.')
        self.assertEqual(resenha.nota, 4)
        self.assertEqual(resenha.usuario, self.user)
        self.assertEqual(resenha.livro, self.livro)
