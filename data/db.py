import sqlite3

def connect():
    return sqlite3.connect("data/sorteador.db")

conn = connect()
cur = conn.cursor()

cur.execute("""

    CREATE TABLE IF NOT EXISTS "aluno" (
        "num"	INTEGER,
        "nome"	TEXT NOT NULL,
        "telefone"	TEXT NOT NULL,
        "instituicao"	TEXT NOT NULL,
        "validado"	INTEGER NOT NULL,
        "sorteado"	INTEGER NOT NULL,
        PRIMARY KEY("num")
)
""")