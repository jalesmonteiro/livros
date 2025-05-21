from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('registrar/', views.registrar, name='registrar'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('<int:id>/', views.detalhe_livro, name='detalhe_livro'),
    path('buscar_livros/', views.buscar_livros, name='buscar_livros'),
    path('listar_livros/', views.listar_livros, name='listar_livros'),
    path('adicionar_livro/', views.adicionar_livro, name='adicionar_livro'),
    path('<int:id>/resenha/', views.adicionar_resenha, name='adicionar_resenha'),
    path('<int:id>/editar/', views.editar_livro, name='editar_livro'),
]
