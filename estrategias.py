class CruzamentoMediasMoveis:
    def __init__(self, janela_curta=21, janela_longa=50):
        self.janela_curta = janela_curta
        self.janela_longa = janela_longa
        self.nome = f"Cruzamento MM ({janela_curta} x {janela_longa})"

    def gerar_sinais(self, df_original):
        print(f"Gerando sinais para a estratégia: {self.nome}...")
        df = df_original.copy()
        df['SMA_curta'] = df['Close'].rolling(window=self.janela_curta).mean()
        df['SMA_longa'] = df['Close'].rolling(window=self.janela_longa).mean()
        df['Sinal'] = 0
        df.dropna(inplace=True)

        condicao_compra = (df['SMA_curta'] > df['SMA_longa']) & (df['SMA_curta'].shift(1) <= df['SMA_longa'].shift(1))
        condicao_venda = (df['SMA_curta'] < df['SMA_longa']) & (df['SMA_curta'].shift(1) >= df['SMA_longa'].shift(1))

        df.loc[condicao_compra, 'Sinal'] = 1
        df.loc[condicao_venda, 'Sinal'] = -1

        return df