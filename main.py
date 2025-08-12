import yfinance as yf
import matplotlib.pyplot as plt
import click
from estrategias import CruzamentoMediasMoveis
from backtester import Backtester
import database

@click.command()
@click.option('--ativo', type=str, required=True, help='Código do ativo. Ex: VALE3.SA')
@click.option('--inicio', type=str, required=True, help='Data de início no formato AAAA-MM-DD')
@click.option('--fim', type=str, required=True, help='Data de fim no formato AAAA-MM-DD')
@click.option('--capital', type=float, default=10000, help='Capital inicial para o backtest.')
def main(ativo, inicio, fim, capital):
    print("--- Argumentos Recebidos ---")
    print(f"Ativo: {ativo}")
    print(f"Data de Inicio: {inicio}")
    print(f"Data de Fim: {fim}")
    print(f"Capital Inicial: {capital}")
    print("Baixando dados do Yahoo Finance...")
    
    conn = database.conectar()
    database.criar_tabelas(conn)
    conn.close()

    click.echo(click.style(f"Executando backtest para {ativo}...", fg='yellow'))

    dados = yf.download(ativo, start=inicio, end=fim, auto_adjust=True)
    estrategia_mm = CruzamentoMediasMoveis(janela_curta=21, janela_longa=50)
    motor = Backtester(dados, capital, estrategia_mm)
    motor._rodar_backtest()

    salvar_resultados(motor, {
        'ativo': ativo,
        'inicio': inicio,
        'fim': fim
    })

    click.echo(click.style("Resultados salvos no banco de dados com sucesso!", fg='green'))

def salvar_resultados(backtester, params):
    conn = database.conectar()
    cursor = conn.cursor()

    sql_sumario = '''
        INSERT INTO tabela_backtests (ativo, estrategia, data_inicio, data_fim, capital_inicial, resultado_final)
        VALUES (?, ?, ?, ?, ?, ?)
    '''

    valores_sumario = (
        params['ativo'],
        backtester.estrategia.nome,
        params['inicio'],
        params['fim'],
        backtester.capital_inicial,
        backtester.capital
    )
    cursor.execute(sql_sumario, valores_sumario)
    backtest_id = cursor.lastrowid

    trades_para_salvar = []
    for trade in backtester.trades:
        trade_tupla = (
            backtest_id,
            trade['data_compra'],
            trade['preco_compra'],
            trade['data_venda'],
            trade['preco_venda'],
            trade['n_acoes'],
        )
        trades_para_salvar.append(trade_tupla)

    sql_trades = '''
        INSERT INTO tabela_trades (backtest_id, data_compra, preco_compra, data_venda, preco_venda, n_acoes)
        VALUES (?, ?, ?, ?, ?, ?)
    '''
    cursor.executemany(sql_trades, trades_para_salvar)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()