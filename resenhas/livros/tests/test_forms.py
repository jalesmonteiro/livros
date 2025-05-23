from django.test import TestCase
from livros.forms import LivroForm, ResenhaForm

class FormTests(TestCase):
    def test_livro_form_valido(self):
        form = LivroForm(data={
            'titulo': 'Memórias Póstumas',
            'autor': 'Machado de Assis',
            'data_publicacao': '1881-01-01'
        })
        self.assertTrue(form.is_valid())

    def test_resenha_form_invalido(self):
        form = ResenhaForm(data={'texto': 'Ótimo livro', 'nota': 6})  # Nota > 5
        self.assertFalse(form.is_valid())
        self.assertIn('nota', form.errors)
