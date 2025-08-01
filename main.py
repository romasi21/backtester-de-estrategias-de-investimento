import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

class Backtester:
    def __init__(self, df, capital_inicial):
        self.df = df.dropna()
        self.capital_inicial = capital_inicial
        self.capital = capital_inicial
        self.n_acoes = 0
        self.trades = []
        self.posicao = False

    def rodar_backtest(self): #itera todos os dias do df checando os sinais
        print("Iniciando backtest...")
        for indice, linha in self.df.iterrows():
            self._checar_sinais(indice, linha)
        print("Backtest finalizado.")
        print(f"Resultado final: R$ {(self.capital + self.n_acoes * self.df['Close'].iloc[-1].item()):.2f}")
        
    def _checar_sinais(self, data, dia_atual): #compara as médias móveis para cada dia e gera um sinal se necessário
        posicao_atual = self.df.index.get_loc(data)
        if posicao_atual == 0:
            return
        dia_anterior = self.df.iloc[posicao_atual - 1]
        
        if dia_atual['SMA_curta'].item() > dia_atual['SMA_longa'].item() and dia_anterior['SMA_curta'].item() <= dia_anterior['SMA_longa'].item() and not self.posicao:
            preco_compra = dia_atual['Close'].item()
            self._executar_compra(data.date(), preco_compra)
            
        elif dia_atual['SMA_curta'].item() < dia_atual['SMA_longa'].item() and dia_anterior['SMA_curta'].item() >= dia_anterior['SMA_longa'].item() and self.posicao:
            preco_venda = dia_atual['Close'].item()
            self._executar_venda(data.date(), preco_venda)

    def _executar_compra(self, data, preco): #executa uma compra
        self.posicao = True
        self.trades.append({'data_compra': data, 'preco_compra': preco})
        self.n_acoes = self.capital // preco
        self.capital -= self.n_acoes * preco
        
    def _executar_venda(self, data, preco): #executa uma venda
        self.posicao = False
        self.trades.append({'data_venda': data, 'preco_venda': preco})
        self.capital += self.n_acoes * preco
        self.n_acoes = 0
        

codigo_ativo = input("Insira o código de um ativo (ex: VALE3.SA): ")
inicio = input("Início do período (ex: 2020-01-01): ")
fim = input("Final do período (ex: 2023-12-31): ")

dados = yf.download(codigo_ativo, start=inicio, end=fim)
dados['SMA_curta'] = dados['Close'].rolling(window=21).mean()
dados['SMA_longa'] = dados['Close'].rolling(window=50).mean()

ativo_1 = Backtester(dados, 10000)
ativo_1.rodar_backtest()
print(f"trades do ativo_1: {ativo_1.trades}")

plt.plot(ativo_1.df['Close'], label=f"Preco de fechamento ({codigo_ativo})")
plt.plot(ativo_1.df['SMA_curta'], label='Media movel curta')
plt.plot(ativo_1.df['SMA_longa'], label='Media movel longa')

plt.title('Preco de Fechamento vs Media Movel')
plt.xlabel('Data')
plt.xticks(rotation=45)
plt.ylabel('Preco (R$)')
plt.legend()
plt.grid(True)
plt.savefig('grafico.png')