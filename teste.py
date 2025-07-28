import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

codigo_ativo = 'VALE3.SA'
inicio = '2024-01-01'
fim = '2025-06-01'

dados = yf.download(codigo_ativo, start=inicio, end=fim)
dados['SMA_curta'] = dados['Close'].rolling(window=21).mean()
dados['SMA_longa'] = dados['Close'].rolling(window=50).mean()

df_exemplo = dados.head(5) 

print("--- Usando .iterrows() ---")
for indice, linha in df_exemplo.iterrows():
    print(f"Data (o índice): {indice.date()}")
    print(f"Preço de Fechamento (na linha): {linha['Close'].item()}")
    print("-" * 20)