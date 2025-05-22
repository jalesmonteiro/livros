import random
from sqlalchemy import (
    Column, Integer, String, Date, Text, ForeignKey, DateTime, Table
)
from sqlalchemy.orm import (
    declarative_base, relationship, Mapped, mapped_column
)
from sqlalchemy.sql import func

Base = declarative_base()

def gerar_cor_hex():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

# Associação Many-to-Many entre Livro e Tag
livro_tag = Table(
    "livros_livro_tags",
    Base.metadata,
    Column("livro_id", ForeignKey("livros_livro.id"), primary_key=True),
    Column("tag_id", ForeignKey("livros_tag.id"), primary_key=True)
)

class Tag(Base):
    __tablename__ = "livros_tag"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(50), unique=True)
    cor: Mapped[str] = mapped_column(String(7), default=gerar_cor_hex)

    livros = relationship("Livro", secondary=livro_tag, back_populates="tags")

    def __repr__(self):
        return f"<Tag(nome={self.nome}, cor={self.cor})>"

class Livro(Base):
    __tablename__ = "livros_livro"

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(200))
    autor: Mapped[str] = mapped_column(String(100))
    data_publicacao: Mapped[Date]
    sinopse: Mapped[str] = mapped_column(Text, nullable=True)
    capa: Mapped[str] = mapped_column(String(200), nullable=True)  # Caminho do arquivo/imagem

    tags = relationship("Tag", secondary=livro_tag, back_populates="livros")
    resenhas = relationship("Resenha", back_populates="livro", cascade="all, delete-orphan")

    def lista_tags(self):
        return [tag.nome for tag in self.tags]

    def media_avaliacoes(self):
        if self.resenhas:
            return round(sum(r.nota for r in self.resenhas) / len(self.resenhas), 2)
        return None

    def __repr__(self):
        return f"<Livro(titulo={self.titulo}, autor={self.autor})>"

class Resenha(Base):
    __tablename__ = "livros_resenha"

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("auth_user.id"))
    livro_id: Mapped[int] = mapped_column(ForeignKey("livros_livro.id"))
    texto: Mapped[str] = mapped_column(Text)
    nota: Mapped[int] = mapped_column(Integer)  # 1 a 5
    data_publicacao: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    livro = relationship("Livro", back_populates="resenhas")
    # O relacionamento com usuário depende do seu modelo de usuário

    def __repr__(self):
        return f"<Resenha(livro_id={self.livro_id}, usuario_id={self.usuario_id}, nota={self.nota})>"
