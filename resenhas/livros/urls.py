from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>/', views.detalhe_livro, name='detalhe_livro'),
    path('buscar_livros/', views.buscar_livros, name='buscar_livros'),
    path('listar_livros/', views.listar_livros, name='listar_livros'),
    path('adicionar_livro/', views.adicionar_livro, name='adicionar_livro'),
    path('<int:id>/resenha/', views.adicionar_resenha, name='adicionar_resenha'),
    path('<int:id>/editar/', views.editar_livro, name='editar_livro'),
    path('<int:id>/excluir/', views.excluir_livro, name='excluir_livro'),
    path('resenha/<int:id>/excluir/', views.excluir_resenha, name='excluir_resenha'),
    path('buscar/', views.buscar_livros, name='buscar_livros'),
]
