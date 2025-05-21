from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *

def registrar(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Faz login automático após cadastro (opcional)
            return redirect('home')  # Altere 'home' para a sua página inicial
    else:
        form = RegistroForm()
    return render(request, 'livros/registro.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    return render(request, 'livros/login.html')

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')

    livros_destaque = Livro.objects.order_by('-id')[:4] 
    resenhas_recentes = Resenha.objects.select_related('livro', 'usuario').order_by('-data_publicacao')[:5]
    context = {
        'livros_destaque': livros_destaque,
        'resenhas_recentes': resenhas_recentes,
    }
    return render(request, 'livros/home.html', context)

def buscar_livros(request):
    return render(request, 'livros/home.html')

def detalhe_livro(request, id):
    livro = get_object_or_404(Livro, id=id)
    resenhas = livro.resenha_set.select_related('usuario').order_by('-data_publicacao')
    return render(request, 'livros/detalhe_livro.html', {
        'livro': livro,
        'resenhas': resenhas,
    })

def listar_livros(request):
    livros = Livro.objects.all().order_by('-id')  # Ordena do mais recente para o mais antigo
    return render(request, 'livros/listar_livros.html', {'livros': livros})

@login_required
def adicionar_livro(request):
    if request.method == "POST":
        form = LivroForm(request.POST, request.FILES)
        if form.is_valid():
            livro = form.save()
            return redirect('detalhe_livro', id=livro.id)
    else:
        form = LivroForm()
    return render(request, 'livros/adicionar_livro.html', {'form': form})

@login_required
def adicionar_resenha(request, id):
    livro = get_object_or_404(Livro, id=id)
    if request.method == "POST":
        form = ResenhaForm(request.POST)
        if form.is_valid():
            resenha = form.save(commit=False)
            resenha.livro = livro
            resenha.usuario = request.user
            resenha.save()
            return redirect('detalhe_livro', id=livro.id)
    else:
        form = ResenhaForm()
    return render(request, 'livros/adicionar_resenha.html', {'form': form, 'livro': livro})

def editar_livro(request, id):
    return render(request, 'livros/home.html')