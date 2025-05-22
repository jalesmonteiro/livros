-- Limpar todas as tabelas (exceto auth_user)
DELETE FROM livros_resenha;
DELETE FROM livros_livro_tags;
DELETE FROM livros_livro;
DELETE FROM livros_tag;

-- Manter apenas o primeiro usuário
DELETE FROM auth_user WHERE id != 1;

-- Usuários fictícios (auth_user)
INSERT INTO auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES
(2, 'pbkdf2_sha256$260000$senha2', NULL, 0, 'joao', 'João', 'Souza', 'joao@email.com', 0, 1, '2024-01-02'),
(3, 'pbkdf2_sha256$260000$senha3', NULL, 0, 'maria', 'Maria', 'Fernandes', 'maria@email.com', 0, 1, '2024-01-03'),
(4, 'pbkdf2_sha256$260000$senha4', NULL, 0, 'pedro', 'Pedro', 'Almeida', 'pedro@email.com', 0, 1, '2024-01-04'),
(5, 'pbkdf2_sha256$260000$senha5', NULL, 0, 'juliana', 'Juliana', 'Costa', 'juliana@email.com', 0, 1, '2024-01-05');

-- Tags
INSERT INTO livros_tag (id, nome, cor) VALUES
(1, 'Clássico', '#e14623'),
(2, 'Literatura', '#4a90e2'),
(3, 'Aventura', '#27ae60'),
(4, 'Romance', '#f39c12'),
(5, 'Fantasia', '#8e44ad'),
(6, 'Drama', '#d35400'),
(7, 'Distopia', '#c0392b'),
(8, 'Mistério', '#34495e'),
(9, 'Ficção', '#16a085'),
(10, 'Épico', '#2c3e50'),
(11, 'Revolução', '#7f8c8d');

-- Livros
INSERT INTO livros_livro (id, titulo, autor, data_publicacao, sinopse, capa) VALUES
(1, 'O Castelo Mágico', 'Maria Oliveira', '2020-05-10', 'Uma aventura em um castelo cheio de segredos.', NULL),
(2, 'Amor nas Estrelas', 'Carlos Lima', '2022-02-14', 'Uma história de romance intergaláctico.', NULL),
(3, 'O Enigma do Relógio', 'Fernanda Dias', '2021-10-01', 'Um mistério envolvendo um antigo relógio.', NULL),
(4, 'Dom Quixote', 'Miguel de Cervantes', '1605-01-16', 'A história do cavaleiro andante Dom Quixote e seu fiel escudeiro Sancho Pança.', NULL),
(5, 'Guerra e Paz', 'Liev Tolstói', '1869-01-01', 'Um épico romance histórico que narra a vida da aristocracia russa.', NULL),
(6, 'Orgulho e Preconceito', 'Jane Austen', '1813-01-28', 'Um romance sobre as dificuldades das mulheres na sociedade inglesa.', NULL),
(7, 'Moby Dick', 'Herman Melville', '1851-10-18', 'A obsessiva caça à baleia branca Moby Dick.', NULL),
(8, 'O Grande Gatsby', 'F. Scott Fitzgerald', '1925-04-10', 'A decadência da alta sociedade americana nos anos 20.', NULL),
(9, 'Crime e Castigo', 'Fiódor Dostoiévski', '1866-01-01', 'A luta moral de um jovem estudante após cometer um assassinato.', NULL),
(10, 'Jane Eyre', 'Charlotte Brontë', '1847-10-16', 'A vida e os desafios da órfã Jane Eyre.', NULL),
(11, 'Os Miseráveis', 'Victor Hugo', '1862-01-01', 'A luta pela redenção de Jean Valjean na França do século XIX.', NULL),
(12, 'O Apanhador no Campo de Centeio', 'J.D. Salinger', '1951-07-16', 'A história de Holden Caulfield e sua rebeldia adolescente.', NULL),
(13, 'A Metamorfose', 'Franz Kafka', '1915-10-01', 'A transformação surreal de Gregor Samsa em um inseto.', NULL),
(14, 'O Senhor dos Anéis', 'J.R.R. Tolkien', '1954-07-29', 'A jornada épica para destruir o Anel do Poder.', NULL),
(15, 'Cem Anos de Solidão', 'Gabriel García Márquez', '1967-05-30', 'A saga da família Buendía na cidade fictícia de Macondo.', NULL),
(16, 'O Morro dos Ventos Uivantes', 'Emily Brontë', '1847-12-01', 'Uma história de amor e vingança na Inglaterra rural.', NULL),
(17, 'Drácula', 'Bram Stoker', '1897-05-26', 'A lenda do vampiro Conde Drácula.', NULL),
(18, 'Frankenstein', 'Mary Shelley', '1818-01-01', 'A criação de um monstro por um cientista.', NULL),
(19, 'O Retrato de Dorian Gray', 'Oscar Wilde', '1890-06-20', 'A história de um homem que mantém sua juventude enquanto seu retrato envelhece.', NULL),
(20, 'O Sol é para Todos', 'Harper Lee', '1960-07-11', 'Um olhar sobre o racismo e a injustiça no sul dos EUA.', NULL),
(21, 'A Revolução dos Bichos', 'George Orwell', '1945-08-17', 'Uma fábula política sobre a corrupção do poder.', NULL),
(22, '1984', 'George Orwell', '1949-06-08', 'Uma distopia sobre um regime totalitário e vigilância.', NULL),
(23, 'O Hobbit', 'J.R.R. Tolkien', '1937-09-21', 'A aventura de Bilbo Bolseiro para recuperar um tesouro.', NULL);

-- Relacionamento Livro-Tags (ManyToMany)
INSERT INTO livros_livro_tags (livro_id, tag_id) VALUES
(1,1),(1,2),(1,3),
(2,1),(2,2),(2,6),
(3,1),(3,2),(3,4),(3,6),
(4,1),(4,2),(4,3),(4,9),
(5,1),(5,2),(5,4),(5,6),
(6,1),(6,2),(6,6),(6,8),
(7,1),(7,2),(7,4),(7,6),
(8,1),(8,2),(8,6),
(9,1),(9,2),(9,6),
(10,1),(10,2),(10,9),
(11,1),(11,2),(11,5),(11,10),(11,3),
(12,1),(12,2),(12,6),(12,9),
(13,1),(13,2),(13,4),(13,6),
(14,1),(14,2),(14,8),(14,9),
(15,1),(15,2),(15,9),(15,8),
(16,1),(16,2),(16,6),(16,9),
(17,1),(17,2),(17,6),
(18,1),(18,2),(18,7),(18,11),
(19,1),(19,2),(19,7),(19,9),
(20,1),(20,2),(20,5),(20,3),(20,10),
(21,1),(21,2),(21,11),
(22,1),(22,2),(22,7),
(23,1),(23,2),(23,5),(23,3),(23,10);

-- Resenhas
INSERT INTO livros_resenha (id, usuario_id, livro_id, texto, nota, data_publicacao) VALUES
(1, 1, 1, 'Adorei a história, cheia de magia e surpresas!', 5, '2024-05-15 10:00:00'),
(2, 2, 1, 'Muito criativo, mas achei o final previsível.', 4, '2024-05-16 15:30:00'),
(3, 1, 2, 'Um romance diferente, gostei bastante.', 4, '2024-05-17 09:10:00'),
(4, 2, 3, 'O mistério me prendeu do início ao fim!', 5, '2024-05-18 20:45:00'),
(5, 1, 4, 'Dom Quixote é uma obra-prima, cheia de humor e aventura. Recomendo a todos!', 5, '2025-05-20 10:00:00'),
(6, 2, 5, 'Guerra e Paz é um livro denso, mas a profundidade dos personagens compensa.', 4, '2025-05-20 11:00:00'),
(7, 3, 6, 'Orgulho e Preconceito é um romance encantador, com personagens marcantes.', 5, '2025-05-20 12:00:00'),
(8, 4, 7, 'Moby Dick tem descrições incríveis do mar, mas achei a leitura um pouco cansativa.', 3, '2025-05-20 13:00:00'),
(9, 5, 8, 'O Grande Gatsby retrata muito bem a decadência dos anos 20. Excelente!', 5, '2025-05-20 14:00:00'),
(10, 1, 9, 'Crime e Castigo é intenso e faz pensar sobre moralidade e justiça.', 5, '2025-05-20 15:00:00'),
(11, 2, 10, 'Jane Eyre é uma heroína inspiradora. Adorei a escrita da Brontë.', 4, '2025-05-20 16:00:00'),
(12, 3, 11, 'Os Miseráveis é emocionante e muito bem escrito. Recomendo!', 5, '2025-05-20 17:00:00'),
(13, 4, 12, 'O Apanhador no Campo de Centeio tem uma narrativa única, gostei bastante.', 4, '2025-05-20 18:00:00'),
(14, 5, 13, 'A Metamorfose é perturbadora e genial ao mesmo tempo.', 5, '2025-05-20 19:00:00'),
(15, 1, 14, 'O Senhor dos Anéis é o melhor épico de fantasia já escrito.', 5, '2025-05-20 20:00:00'),
(16, 2, 15, 'Cem Anos de Solidão tem uma atmosfera mágica e envolvente.', 5, '2025-05-20 21:00:00'),
(17, 3, 16, 'O Morro dos Ventos Uivantes é intenso e cheio de reviravoltas.', 4, '2025-05-20 22:00:00'),
(18, 4, 17, 'Drácula é um clássico do terror, leitura obrigatória para fãs do gênero.', 5, '2025-05-20 23:00:00'),
(19, 5, 18, 'Frankenstein levanta questões profundas sobre ética e ciência.', 4, '2025-05-21 09:00:00'),
(20, 1, 19, 'O Retrato de Dorian Gray é fascinante e sombrio.', 5, '2025-05-21 10:00:00'),
(21, 2, 20, 'O Sol é para Todos é um livro sensível e necessário.', 5, '2025-05-21 11:00:00'),
(22, 3, 21, 'A Revolução dos Bichos é uma alegoria brilhante sobre poder.', 4, '2025-05-21 12:00:00'),
(23, 4, 22, '1984 é assustadoramente atual. Um clássico indispensável.', 5, '2025-05-21 13:00:00'),
(24, 5, 23, 'O Hobbit é uma aventura deliciosa do começo ao fim.', 5, '2025-05-21 14:00:00');
