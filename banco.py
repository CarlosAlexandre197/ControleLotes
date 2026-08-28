import sqlite3
import os


# ============================================================
# CONFIGURAÇÃO DO BANCO
# ============================================================

PASTA_DB = "database"
ARQUIVO_DB = os.path.join(
    PASTA_DB,
    "controle_lotes.db"
)


# ============================================================
# CONEXÃO
# ============================================================

def conectar():

    if not os.path.exists(PASTA_DB):
        os.makedirs(PASTA_DB)

    return sqlite3.connect(ARQUIVO_DB)


# ============================================================
# CRIAÇÃO / ATUALIZAÇÃO DAS TABELAS
# ============================================================

def criar_tabela():

    conn = conectar()
    cursor = conn.cursor()

    # --------------------------------------------------------
    # TABELA DE LOTES
    # --------------------------------------------------------

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

            data TEXT,

            status TEXT,

            faturado INTEGER DEFAULT 0,

            embarcado INTEGER DEFAULT 0,

            pre_autorizacao INTEGER DEFAULT 0,

            notas_impressas INTEGER DEFAULT 0
        )
    """)

    # --------------------------------------------------------
    # TABELA OMNICHANNEL
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS omnichannel (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            quantidade INTEGER,

            data TEXT,

            hora TEXT
        )
    """)

    conn.commit()

    # --------------------------------------------------------
    # ATUALIZAÇÃO DO BANCO EXISTENTE
    #
    # Se o banco já existia antes das novas colunas,
    # adicionamos somente as colunas que estiverem faltando.
    # --------------------------------------------------------

    cursor.execute("PRAGMA table_info(lotes)")

    colunas_existentes = [
        coluna[1]
        for coluna in cursor.fetchall()
    ]

    novas_colunas = {
    "status":
        "TEXT DEFAULT 'Pendente'",

    "faturado":
        "INTEGER DEFAULT 0",

    "embarcado":
        "INTEGER DEFAULT 0",

    "pre_autorizacao":
        "INTEGER DEFAULT 0",

    "notas_impressas":
        "INTEGER DEFAULT 0"
    }
    
    for nome_coluna, tipo in novas_colunas.items():

        if nome_coluna not in colunas_existentes:

            cursor.execute(
                f"""
                ALTER TABLE lotes
                ADD COLUMN {nome_coluna} {tipo}
                """
            )

    conn.commit()
    conn.close()


# ============================================================
# SALVAR LOTE
#
# Neste momento salvamos somente:
# lote
# quantidade
# cartões
# cancelados
# quantidade final
#
# Palete, montador e caixas serão preenchidos posteriormente.
# ============================================================

def salvar_lote(
    lote,
    quantidade,
    cartoes,
    cancelados,
    final,
    data,
    status="Pendente"
):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO lotes
        (
            lote,
            quantidade,
            cartoes,
            cancelados,
            final,
            data,
            status,
            faturado,
            embarcado,
            pre_autorizacao,
            notas_impressas
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, 0, 0, 0, 0)
    """, (
        lote,
        quantidade,
        cartoes,
        cancelados,
        final,
        data,
        status
    ))

    conn.commit()
    conn.close()


# ============================================================
# ATUALIZAR DADOS DA SEPARAÇÃO
#
# Depois que o lote for separado, preenchermos:
# palete
# montador
# caixas
#
# O status passa para "Finalizado".
# ============================================================

def atualizar_separacao(
    lote,
    palete,
    montador,
    caixas
):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE lotes
        SET
            palete = ?,
            montador = ?,
            caixas = ?,
            status = 'Finalizado'
        WHERE lote = ?
    """, (
        palete,
        montador,
        caixas,
        lote
    ))

    conn.commit()
    conn.close()


# ============================================================
# ATUALIZAR STATUS DO PÓS-SEPARAÇÃO
# ============================================================

def atualizar_status_lote(
    lote,
    faturado,
    embarcado,
    pre_autorizacao,
    notas_impressas
):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE lotes
        SET
            faturado = ?,
            embarcado = ?,
            pre_autorizacao = ?,
            notas_impressas = ?
        WHERE lote = ?
    """, (
        int(faturado),
        int(embarcado),
        int(pre_autorizacao),
        int(notas_impressas),
        lote
    ))

    conn.commit()
    conn.close()


# ============================================================
# BUSCAR LOTES DO DIA
#
# Retorna também os quatro controles:
# faturado
# embarcado
# pré-autorização
# notas fiscais
# ============================================================

def buscar_lotes_do_dia(data):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            lote,
            quantidade,
            cartoes,
            cancelados,
            final,
            palete,
            montador,
            caixas,
            status,
            faturado,
            embarcado,
            pre_autorizacao,
            notas_impressas

        FROM lotes

        WHERE data = ?

        ORDER BY id
    """, (data,))

    dados = cursor.fetchall()

    conn.close()

    return dados


# ============================================================
# BUSCAR UM LOTE ESPECÍFICO
# ============================================================

def buscar_lote(lote):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            lote,
            quantidade,
            cartoes,
            cancelados,
            final,
            palete,
            montador,
            caixas,
            data,
            status,
            faturado,
            embarcado,
            pre_autorizacao,
            notas_impressas

        FROM lotes

        WHERE lote = ?

        LIMIT 1
    """, (lote,))

    dado = cursor.fetchone()

    conn.close()

    return dado


# ============================================================
# CONTAR LOTES
# ============================================================

def contar_lotes():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM lotes"
    )

    total = cursor.fetchone()[0]

    conn.close()

    return total


# ============================================================
# EXCLUIR LOTE
# ============================================================

def excluir_lote_db(lote):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM lotes WHERE lote = ?",
        (lote,)
    )

    conn.commit()
    conn.close()


# ============================================================
# SALVAR OMNICHANNEL
# ============================================================

def salvar_omni(
    quantidade,
    data,
    hora
):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO omnichannel
        (
            quantidade,
            data,
            hora
        )
        VALUES (?, ?, ?)
    """, (
        quantidade,
        data,
        hora
    ))

    conn.commit()
    conn.close()


# ============================================================
# BUSCAR OMNICHANNEL DO DIA
# ============================================================

def buscar_omni_do_dia(data):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            quantidade,
            hora

        FROM omnichannel

        WHERE data = ?

        ORDER BY id
    """, (data,))

    dados = cursor.fetchall()

    conn.close()

    return dados


# ============================================================
# EXCLUIR OMNICHANNEL
# ============================================================

def excluir_omni(id_omni):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM omnichannel WHERE id = ?",
        (id_omni,)
    )

    conn.commit()
    conn.close()


# ============================================================
# ATUALIZAR OMNICHANNEL
# ============================================================

def atualizar_omni(
    id_omni,
    quantidade
):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE omnichannel
        SET quantidade = ?
        WHERE id = ?
    """, (
        quantidade,
        id_omni
    ))

    conn.commit()
    conn.close()


# ============================================================
# INICIALIZAÇÃO DO BANCO
# ============================================================

criar_tabela()