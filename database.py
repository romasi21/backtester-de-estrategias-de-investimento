import sqlite3

def conectar():
    conn = sqlite3.connect('backtests.db')
    return conn

def criar_tabelas(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tabela_backtests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ativo TEXT NOT NULL,
            estrategia TEXT NOT NULL,
            data_inicio TEXT NOT NULL,
            data_fim TEXT NOT NULL,
            capital_inicial REAL NOT NULL,
            resultado_final REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tabela_trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            backtest_id INTEGER NOT NULL,
            data_compra TEXT NOT NULL,
            preco_compra REAL NOT NULL,
            data_venda TEXT NOT NULL,
            preco_venda REAL NOT NULL,
            n_acoes INTEGER NOT NULL,
            FOREIGN KEY (backtest_id) REFERENCES tabela_backtests (id)
        )
    ''')

    print("Tabelas verificadas/criadas com sucesso.")
    conn.commit()