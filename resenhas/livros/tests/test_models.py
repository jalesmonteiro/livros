from django.test import TestCase, override_settings
from django.contrib.auth.models import User
from livros.models import Tag, Livro, Resenha
from datetime import date
import tempfile
import shutil
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
import io
from PIL import Image

@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class ModelosTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        # Limpa arquivos de upload após os testes
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.tag1 = Tag.objects.create(nome="Ficção")
        self.tag2 = Tag.objects.create(nome="Clássico")
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.livro = Livro.objects.create(
            titulo="Dom Casmurro",
            autor="Machado de Assis",
            data_publicacao=date(1899, 1, 1)
        )
        self.livro.tags.add(self.tag1, self.tag2)

    def test_tag_str(self):
        self.assertEqual(str(self.tag1), "Ficção")
        self.assertTrue(self.tag1.cor.startswith("#") and len(self.tag1.cor) == 7)

    def test_livro_str(self):
        self.assertEqual(str(self.livro), "Dom Casmurro (Machado de Assis)")

    def test_lista_tags(self):
        self.assertEqual(set(self.livro.lista_tags), set(["Ficção", "Clássico"]))

    def test_media_avaliacoes(self):
        # Sem resenhas
        self.assertIsNone(self.livro.media_avaliacoes())
        # Com resenhas
        Resenha.objects.create(usuario=self.user, livro=self.livro, texto="Ótimo", nota=5)
        Resenha.objects.create(usuario=self.user, livro=self.livro, texto="Bom", nota=3)
        self.assertEqual(self.livro.media_avaliacoes(), 4.0)

    def test_resenha_str(self):
        resenha = Resenha.objects.create(usuario=self.user, livro=self.livro, texto="Excelente", nota=5)
        self.assertEqual(str(resenha), f"Resenha de {self.livro} por {self.user.username}")

    def test_livro_tags_relationship(self):
        self.assertEqual(self.livro.tags.count(), 2)
        self.assertIn(self.tag1, self.livro.tags.all())

    def test_livro_capa_upload_e_delete(self):
        # Cria uma imagem fake em memória
        image_io = io.BytesIO()
        image = Image.new("RGB", (100, 100), color="blue")
        image.save(image_io, format="JPEG")
        image_io.seek(0)
        capa_simulada = SimpleUploadedFile("capa.jpg", image_io.read(), content_type="image/jpeg")
        self.livro.capa = capa_simulada
        self.livro.save()
        caminho_arquivo = self.livro.capa.path
        self.assertTrue(self.livro.capa.name.startswith("capas/livro_"))
        # Testa se o arquivo realmente existe
        import os
        self.assertTrue(os.path.exists(caminho_arquivo))
        # Testa delete (arquivo deve ser removido)
        self.livro.delete()
        self.assertFalse(os.path.exists(caminho_arquivo))

    def test_tag_nome_unico(self):
        with self.assertRaises(Exception):
            Tag.objects.create(nome="Ficção")
