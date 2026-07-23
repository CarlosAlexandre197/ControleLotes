import sqlite3
import os

PASTA_DB = "database"
ARQUIVO_DB = os.path.join(PASTA_DB, "controle_lotes.db")


def conectar():
    if not os.path.exists(PASTA_DB):
        os.makedirs(PASTA_DB)

    return sqlite3.connect(ARQUIVO_DB)


def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS lotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lote TEXT,
        quantidade INTEGER,
        cartoes INTEGER,
        cancelados INTEGER,
        final INTEGER,
        palete TEXT,
        montador TEXT,
        caixas INTEGER,
        data TEXT
    )
    """)

    conn.commit()
    conn.close()


def salvar_lote(
        lote,
        quantidade,
        cartoes,
        cancelados,
        final,
        palete,
        montador,
        caixas,
        data):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO lotes
    (lote, quantidade, cartoes, cancelados,
     final, palete, montador, caixas, data)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        lote,
        quantidade,
        cartoes,
        cancelados,
        final,
        palete,
        montador,
        caixas,
        data
    ))

    conn.commit()
    conn.close()
    
def buscar_lotes_do_dia(data):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT lote, quantidade, cartoes, cancelados,
               final, palete, montador, caixas, data
        FROM lotes
        WHERE data = ?
    """, (data,))

    dados = cursor.fetchall()

    conn.close()

    return dados

def contar_lotes():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM lotes")

    total = cursor.fetchone()[0]

    conn.close()

    return total