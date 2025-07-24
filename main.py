import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

codigo_ativo = input("Insira o código de um ativo (ex: VALE3.SA): ")
inicio = input("Início do período (ex: 2020-01-01): ")
fim = input("Final do período (ex: 2023-12-31): ")

dados = yf.download(codigo_ativo, start=inicio, end=fim)
dados['MMS21'] = dados['Close'].rolling(window=21).mean()
dados['MMS50'] = dados['Close'].rolling(window=50).mean()

plt.plot(dados['Close'], label=f"Preco de fechamento ({codigo_ativo})")
plt.plot(dados['MMS21'], label='Media movel de 21 dias')
plt.plot(dados['MMS50'], label='Media movel de 50 dias')

plt.title('Preco de Fechamento vs Media Movel')
plt.xlabel('Data')
plt.ylabel('Preco (R$)')
plt.legend()
plt.grid(True)
plt.show()