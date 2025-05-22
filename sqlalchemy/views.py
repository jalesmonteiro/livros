# ==== IMPORTAÇÕES DJANGO ====
# Para modelos e queries
from django.db.models import Avg, Q
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from models import Livro, Resenha

# ==== IMPORTAÇÕES SQLALCHEMY ====
# Para sessão, funções e operadores
from sqlalchemy import func, or_

class NotFound(Exception):
    pass

session = None
termo = None
page_number = None
quantidade = None

# 1. Livros em destaque (maior nota média)
#django
livros_destaque = Livro.objects.annotate(media=Avg('resenhas__nota')).order_by('-media')[:4]

#sqlalchemy
from sqlalchemy import func
livros_destaque = (
    session.query(Livro)
    .outerjoin(Livro.resenhas)
    .group_by(Livro.id)
    .add_columns(func.avg(Resenha.nota).label('media'))
    .order_by(func.avg(Resenha.nota).desc())
    .limit(4)
    .all()
)
# livros_destaque será uma lista de tuplas (Livro, media)

# 2. Resenhas recentes (com livro e usuário)
#django
resenhas_recentes = Resenha.objects.select_related('livro', 'usuario').order_by('-data_publicacao')[:5]

#sqlalchemy
resenhas_recentes = (
    session.query(Resenha)
    .join(Resenha.livro)
    .join(Resenha.usuario)
    .order_by(Resenha.data_publicacao.desc())
    .limit(5)
    .all()
)

# 3. Detalhe do livro (buscar livro por id)
#django
livro = get_object_or_404(Livro, id=id)

#sqlalchemy
livro = session.query(Livro).filter_by(id=id).first()
if not livro:
    raise NotFound()

# 4. Resenhas de um livro, ordenadas por data, com usuário
#django
resenhas = livro.resenhas.select_related('usuario').order_by('-data_publicacao')

#sqlalchemy
resenhas = (
    session.query(Resenha)
    .filter_by(livro_id=livro.id)
    .join(Resenha.usuario)
    .order_by(Resenha.data_publicacao.desc())
    .all()
)

# 5. Listar todos os livros, ordenados, para paginação
#django
livros = Livro.objects.all().order_by('-id')

#sqlalchemy
livros = session.query(Livro).order_by(Livro.id.desc()).all()

# 6. Buscar livros por termo (título, autor ou sinopse, case-insensitive)
#django
livros = Livro.objects.all()
if termo:
    livros = livros.filter(
        Q(titulo__icontains=termo) |
        Q(autor__icontains=termo) |
        Q(sinopse__icontains=termo)
    )

#sqlalchemy
from sqlalchemy import or_
query = session.query(Livro)
if termo:
    like = f"%{termo}%"
    query = query.filter(
        or_(
            Livro.titulo.ilike(like),
            Livro.autor.ilike(like),
            Livro.sinopse.ilike(like)
        )
    )
livros = query.all()

# 7. Buscar resenha por id (para exclusão)
#django
resenha = get_object_or_404(Resenha, id=id)

#sqlalchemy
resenha = session.query(Resenha).filter_by(id=id).first()
if not resenha:
    raise NotFound()

# 8. Buscar livro por id (para edição/exclusão)
#django
livro = get_object_or_404(Livro, id=id)

#sqlalchemy
livro = session.query(Livro).filter_by(id=id).first()
if not livro:
    raise NotFound()

# 9. Paginação
#django
paginator = Paginator(livros, quantidade)
page_obj = paginator.get_page(page_number)

#sqlalchemy
# Exemplo: quantidade = 8, page_number = 2
livros = (
    session.query(Livro)
    .order_by(Livro.id.desc())
    .offset((page_number - 1) * quantidade)
    .limit(quantidade)
    .all()
)
