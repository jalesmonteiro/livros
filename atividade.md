# Modelagem e Consultas para Praticar Relacionamentos e SQL no Django ORM

## Modelagem

1. **Perfil de Usuário (OneToOne)**
   > Adicione um modelo `Perfil` com informações extras (bio, avatar, etc.) relacionado 1-para-1 ao modelo `User`.

2. **Editora de Livro (ForeignKey)**
   > Adicione um modelo `Editora` e relacione cada livro a uma editora (1 editora, muitos livros).

3. **Favoritos e Livros Lidos (ManyToMany)**
   > Permita que usuários favoritem livros ou marquem livros como lidos (relacionamento muitos-para-muitos entre usuários e livros).

---

## Consultas

4. **Quantidade de Resenhas por Livro**
   > Mostre a quantidade de resenhas de um livro no template `listar_livros.html` usando `.annotate()` e `Count`.

5. **Média de Notas do Autor**
   > No template `detalhe_livro.html`, mostre a média de notas de todos os livros do autor do livro exibido.

6. **Número da Próxima Resenha**
   > Em "adicionar resenha", substitua o texto por  
   > `"Adicionar a xº Resenha para 'nome do livro'"`,  
   > onde x é o número de resenhas atual do livro + 1.

---

## Avançados

7. **Filtro de Nota**
   > Adicione filtro de nota na busca de livros (exibir apenas livros cuja média de nota seja igual ou superior ao valor escolhido).

8. **Página de Livros Mais Favoritados/Lidos**
   > Crie uma nova página que exiba os livros mais favoritados ou mais lidos.

9. **Página de Estatísticas**
   > Crie uma página de estatísticas mostrando:
   > - Quantidade de livros
   > - Quantidade de resenhas
   > - Quantidade de usuários
   > - Quantidade de tags
   > - Quantidade de autores
   > - Quantidade de editoras
   > - Média de livros lidos/favoritados por usuário
   > - Média de resenhas por livro
   > - Média de tags por livro

---

Essas sugestões vão te ajudar a praticar:
- **Relacionamentos OneToOne, ForeignKey e ManyToMany**
- **Consultas com filtros, anotações (`annotate`), agregações (`Count`, `Avg`)**
- **Uso de funções SQL e lógica de exibição em templates**
- **Criação de páginas dinâmicas e estatísticas com o ORM do Django**

Aproveite para experimentar diferentes tipos de consultas e refinar sua modelagem!
