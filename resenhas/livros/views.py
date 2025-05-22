from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Avg
from django.http import HttpResponseForbidden
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

    livros_destaque = Livro.objects.annotate(media=Avg('resenhas__nota')).order_by('-media')[:4]
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
    resenhas = livro.resenhas.select_related('usuario').order_by('-data_publicacao')
    return render(request, 'livros/detalhe_livro.html', {
        'livro': livro,
        'resenhas': resenhas,
    })

def listar_livros(request):
    # Obtém o parâmetro 'quantidade' da query string, padrão 8
    quantidade = request.GET.get('quantidade', '8')
    try:
        quantidade = int(quantidade)
        if quantidade not in [8, 16, 24]:
            quantidade = 8
    except ValueError:
        quantidade = 8

    livros = Livro.objects.all().order_by('-id')
    paginator = Paginator(livros, quantidade)

    # Obtém o número da página da query string, padrão 1
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'livros/listar_livros.html', {
        'page_obj': page_obj,
        'quantidade': quantidade,
    })

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

@login_required
def editar_livro(request, id):
    livro = get_object_or_404(Livro, id=id)
    if request.method == "POST":
        form = LivroForm(request.POST, request.FILES, instance=livro)
        if form.is_valid():
            form.save()
            return redirect('detalhe_livro', id=livro.id)
    else:
        form = LivroForm(instance=livro)
    return render(request, 'livros/editar_livro.html', {'form': form, 'livro': livro})

@login_required
def excluir_resenha(request, id):
    resenha = get_object_or_404(Resenha, id=id)
    if resenha.usuario != request.user:
        return HttpResponseForbidden("Você não pode excluir esta resenha.")
    livro_id = resenha.livro.id
    if request.method == "POST":
        resenha.delete()
        return redirect('detalhe_livro', id=livro_id)
    return render(request, 'livros/confirmar_exclusao_resenha.html', {'resenha': resenha})

def buscar_livros(request):
    termo = request.GET.get('q', '')
    livros = Livro.objects.all()
    if termo:
        livros = livros.filter(
            Q(titulo__icontains=termo)
            | Q(autor__icontains=termo) 
#            | Q(sinopse__icontains=termo)
        )
    # Pegue a quantidade de itens por página, igual à view de listagem
    quantidade = request.GET.get('quantidade', '8')
    try:
        quantidade = int(quantidade)
        if quantidade not in [8, 16, 24]:
            quantidade = 8
    except ValueError:
        quantidade = 8

    paginator = Paginator(livros, quantidade)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'livros/listar_livros.html', {
        'page_obj': page_obj,
        'quantidade': quantidade,
        'busca': termo,
    })

@login_required
def excluir_livro(request, id):
    livro = get_object_or_404(Livro, id=id)
    if request.method == "POST":
        livro.delete()
        return redirect('listar_livros')
    return render(request, 'livros/confirmar_exclusao_livro.html', {'livro': livro})