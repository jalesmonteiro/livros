# Comparação Django ORM x SQLAlchemy ORM — Consulta a Consulta

Abaixo estão as **semelhanças** e **diferenças** para cada par de consulta Django/SQLAlchemy, seguindo a numeração dos exemplos anteriores:

---

## 1. Livros em destaque (maior nota média)

**Semelhanças:**
- Ambos realizam agregação (média) sobre as notas das resenhas.
- Ambos ordenam os livros pela média e limitam o resultado a 4.

**Diferenças:**
- **Django:** Usa `annotate` e `order_by` de forma declarativa, retornando diretamente objetos Livro com um atributo extra `media`.
- **SQLAlchemy:** Usa `add_columns` para adicionar a média como coluna extra, retornando tuplas (`Livro`, `media`). O join e group by precisam ser explícitos.

---

## 2. Resenhas recentes (com livro e usuário)

**Semelhanças:**
- Ambos buscam as resenhas mais recentes, incluindo dados do livro e do usuário.
- Ambos limitam a quantidade de resultados.

**Diferenças:**
- **Django:** Usa `select_related` para otimizar queries e evitar N+1.
- **SQLAlchemy:** Usa `join` explícito para garantir o carregamento dos dados relacionados.

---

## 3. Detalhe do livro (buscar livro por id)

**Semelhanças:**
- Ambos buscam um único livro pelo ID.

**Diferenças:**
- **Django:** Usa `get_object_or_404`, que já lança 404 automaticamente.
- **SQLAlchemy:** Usa `first()` e é necessário tratar manualmente o caso de não encontrado (raise NotFound ou similar).

---

## 4. Resenhas de um livro, ordenadas por data, com usuário

**Semelhanças:**
- Ambos filtram resenhas pelo livro e ordenam por data.
- Ambos incluem o usuário relacionado.

**Diferenças:**
- **Django:** Usa o related_name (`resenhas`) e `select_related` para otimizar.
- **SQLAlchemy:** Usa `filter_by(livro_id=...)` e `join` explícito para o usuário.

---

## 5. Listar todos os livros, ordenados, para paginação

**Semelhanças:**
- Ambos ordenam os livros por ID decrescente.

**Diferenças:**
- **Django:** Usa `all().order_by()`, retornando um queryset.
- **SQLAlchemy:** Usa `query().order_by().all()`, retornando uma lista.

---

## 6. Buscar livros por termo (título, autor ou sinopse, case-insensitive)

**Semelhanças:**
- Ambos permitem busca parcial e case-insensitive em múltiplos campos.
- Ambos usam lógica OR para combinar os campos.

**Diferenças:**
- **Django:** Usa `Q` objects e `__icontains` para buscas flexíveis.
- **SQLAlchemy:** Usa `or_` e `ilike` para buscas flexíveis.

---

## 7. Buscar resenha por id (para exclusão)

**Semelhanças:**
- Ambos buscam uma resenha pelo ID.

**Diferenças:**
- **Django:** Usa `get_object_or_404` para lançar 404 automaticamente.
- **SQLAlchemy:** Usa `first()` e é necessário tratar manualmente o caso de não encontrado.

---

## 8. Buscar livro por id (para edição/exclusão)

**Semelhanças:**
- Igual ao par anterior, ambos buscam um livro pelo ID.

**Diferenças:**
- **Django:** Usa `get_object_or_404`.
- **SQLAlchemy:** Usa `first()` e trata o caso de não encontrado.

---

## 9. Paginação

**Semelhanças:**
- Ambos retornam apenas um subconjunto dos resultados totais, de acordo com a página e quantidade desejada.

**Diferenças:**
- **Django:** Usa a classe `Paginator` e métodos como `get_page`, que facilitam a integração com templates.
- **SQLAlchemy:** Usa `offset` e `limit` diretamente na query; a lógica de página ativa e total de páginas precisa ser implementada manualmente (ou usando extensões).

---

# Resumo Geral

- **Django ORM** oferece métodos de alto nível, integração com tratamento de erros e paginação pronta para uso, além de otimizações automáticas com `select_related`.
- **SQLAlchemy ORM** exige mais configuração manual, mas oferece controle total sobre joins, agregações e paginação, sendo mais próximo do SQL puro.
- Ambos permitem realizar as mesmas operações, mas a sintaxe, o nível de abstração e a integração com o restante do framework diferem bastante.

