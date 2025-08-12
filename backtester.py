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

        self.capital = (self.capital + self.n_acoes * self.df_com_sinais['Close'].iloc[-1].item())
        print("Backtest finalizado.")
        print(f"Resultado final: R$ {self.capital:.2f}")

    def _executar_compra(self, data, preco):
        self.posicao = True
        self.n_acoes = self.capital // preco
        self.capital -= self.n_acoes * preco
        self.trades.append({'data_compra': data, 'preco_compra': preco, 'data_venda': 0, 'preco_venda': 0, 'n_acoes':self.n_acoes})

    def _executar_venda(self, data, preco):
        self.posicao = False
        self.capital += self.n_acoes * preco
        self.n_acoes = 0
        self.trades.append({'data_compra': 0, 'preco_compra': 0, 'data_venda': data, 'preco_venda': preco, 'n_acoes':self.n_acoes})