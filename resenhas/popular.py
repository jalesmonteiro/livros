import sqlite3

# Caminho para o banco de dados SQLite (ajuste se necessário)
DB_PATH = 'db.sqlite3'
# Caminho para o arquivo SQL
SQL_PATH = 'popular_banco.sql'

def executar_sql(db_path, sql_path):
    with open(sql_path, 'r', encoding='utf-8') as f:
        sql = f.read()
    conn = sqlite3.connect(db_path)
    try:
        with conn:
            conn.executescript(sql)
        print("Script SQL executado com sucesso!")
    except Exception as e:
        print("Erro ao executar o script SQL:", e)
    finally:
        conn.close()

if __name__ == '__main__':
    executar_sql(DB_PATH, SQL_PATH)
