import yfinance as yf
import matplotlib.pyplot as plt
import click
from estrategias import CruzamentoMediasMoveis

class Backtester:
    def __init__(self, df, capital_inicial, estrategia):
        self.df_original = df
        self.df_com_sinais = df
        self.capital_inicial = capital_inicial
        self.capital = capital_inicial
        self.n_acoes = 0
        self.trades = []
        self.posicao = False
        self.estrategia = estrategia

    def _rodar_backtest(self):
        print(f"Iniciando backtest com capital de R$ {self.capital_inicial:.2f}")
        print(f"Usando a estrategia: {self.estrategia.nome}")

        self.df_com_sinais = self.estrategia.gerar_sinais(self.df_original)

        for indice, dia in self.df_com_sinais.iterrows():
            if dia['Sinal'].item() == 1 and not self.posicao:
                self.posicao = True
                self._executar_compra(indice.date(), dia['Close'].item())

            elif dia['Sinal'].item() == -1 and self.posicao:
                self.posicao = False
                self._executar_venda(indice.date(), dia['Close'].item())

        print("Backtest finalizado.")
        print(f"Resultado final: R$ {(self.capital + self.n_acoes * self.df_com_sinais['Close'].iloc[-1].item()):.2f}")

    def _executar_compra(self, data, preco):
        self.posicao = True
        self.trades.append({'data_compra': data, 'preco_compra': preco})
        self.n_acoes = self.capital // preco
        self.capital -= self.n_acoes * preco

    def _executar_venda(self, data, preco):
        self.posicao = False
        self.trades.append({'data_venda': data, 'preco_venda': preco})
        self.capital += self.n_acoes * preco
        self.n_acoes = 0

def gerar_grafico_media_movel(ativo):
    plt.plot(ativo.df_com_sinais['Close'], label="Preco de fechamento")
    plt.plot(ativo.df_com_sinais['SMA_curta'], label='Media movel curta')
    plt.plot(ativo.df_com_sinais['SMA_longa'], label='Media movel longa')

    plt.title('Preco de Fechamento vs Media Movel')
    plt.xlabel('Data')
    plt.xticks(rotation=45)
    plt.ylabel('Preco (R$)')
    plt.legend()
    plt.grid(True)
    plt.savefig('grafico.png')

@click.command()
@click.option('--ativo', type=str, required=True, help='Código do ativo. Ex: VALE3.SA')
@click.option('--inicio', type=str, required=True, help='Data de início no formato AAAA-MM-DD')
@click.option('--fim', type=str, required=True, help='Data de fim no formato AAAA-MM-DD')
@click.option('--capital', type=float, default=10000, help='Capital inicial para o backtest.')
def rodar_aplicacao(ativo, inicio, fim, capital):
    print("--- Argumentos Recebidos ---")
    print(f"Ativo: {ativo}")
    print(f"Data de Inicio: {inicio}")
    print(f"Data de Fim: {fim}")
    print(f"Capital Inicial: {capital}")
    print("Baixando dados do Yahoo Finance...")
    
    dados = yf.download(ativo, start=inicio, end=fim, auto_adjust=True)

    estrat_1 = CruzamentoMediasMoveis(21, 50)
    ativo_1 = Backtester(dados, capital, estrat_1)
    ativo_1._rodar_backtest()
    #gerar_grafico_media_movel(ativo_1)

if __name__ == '__main__':
    rodar_aplicacao()