import sqlite3
import pandas as pd

DB_FILE = "backtests.db"

def visualizar_tabela(nome_tabela):
    try:
        conn = sqlite3.connect(DB_FILE)
        df = pd.read_sql_query(f"SELECT * FROM {nome_tabela}", conn)

        print(f"--- Conteúdo da Tabela: {nome_tabela} ---")
        if df.empty:
            print("A tabela está vazia.")
        else:
            print(df.to_string())
        print("\n")
        
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    visualizar_tabela("tabela_backtests")
    visualizar_tabela("tabela_trades")