# Motor de Backtesting de Estratégias de Investimento

Uma ferramenta de linha de comando (CLI) em Python para simular e avaliar o desempenho de estratégias de trading quantitativo, utilizando dados históricos de mercado. Este projeto foi construído com foco em boas práticas de arquitetura de software, como modularidade e testabilidade.

## ✨ Principais Funcionalidades

* **Backtesting de Estratégias:** Executa simulações de compra e venda baseadas em estratégias predefinidas, calculando o resultado financeiro e o crescimento do capital.
* **Arquitetura Modular e Extensível:** Utiliza Injeção de Dependência para desacoplar o motor de backtesting da lógica da estratégia, permitindo que novas estratégias (como IFR, Bandas de Bollinger, etc.) sejam adicionadas sem alterar o núcleo do sistema.
* **Interface de Linha de Comando (CLI):** Uma CLI robusta e amigável, construída com a biblioteca `Click`, permite a fácil configuração de parâmetros como ativo, período e capital inicial.
* **Persistência de Resultados:** Todos os sumários de backtest e cada trade individual são salvos em um banco de dados **SQL (SQLite)**, criando um histórico permanente para análise posterior.

## 🏗️ Arquitetura do Projeto

O projeto segue uma estrutura inspirada no padrão MVC (Model-View-Controller) para garantir a separação de responsabilidades:

* **Model:** As classes `Backtester` e `Estrategia`, junto com o banco de dados `SQLite`, representam os dados e a lógica de negócio principal.
* **View:** A interface de linha de comando (`main.py` com `Click`) é responsável por interagir com o usuário e exibir os resultados.
* **Controller:** O script principal (`main.py`) orquestra a aplicação, recebendo os inputs da View, instanciando os objetos do Model e iniciando a execução.

## 🛠️ Stack de Tecnologias

* **Python 3.10+**
* **Click:** Para a Interface de Linha de Comando (CLI).
* **Pandas:** Para manipulação e análise de dados em séries temporais.
* **yfinance:** Para a obtenção de dados históricos do mercado de ações.
* **SQLite:** Para o armazenamento relacional dos resultados.

## 🚀 Instalação e Configuração

Para executar este projeto localmente, siga os passos abaixo.

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/romasi21/backtester-de-estrategias-de-investimento.git](https://github.com/romasi21/backtester-de-estrategias-de-investimento.git)
    cd backtester-de-estrategias-de-investimento
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # Para Linux/macOS
    python3 -m venv venv
    source venv/bin/activate

    # Para Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    (Primeiro, certifique-se de ter um arquivo `requirements.txt`. Se não tiver, gere-o com `pip freeze > requirements.txt`)
    ```bash
    pip install -r requirements.txt
    ```

## 📈 Como Usar

A aplicação é executada através da linha de comando.

1.  **Para ver todas as opções disponíveis:**
    ```bash
    python main.py --help
    ```

2.  **Exemplo de execução básica:**
    (Testa a estratégia de cruzamento de médias móveis para PETR4.SA no ano de 2023)
    ```bash
    python main.py --ativo PETR4.SA --inicio 2023-01-01 --fim 2023-12-31
    ```

3.  **Execução com um capital inicial diferente:**
    ```bash
    python main.py --ativo VALE3.SA --inicio 2022-01-01 --fim 2023-12-31 --capital 50000
    ```

Após a execução, os resultados serão impressos no console e um arquivo `backtests.db` será criado (ou atualizado) no diretório raiz com todos os dados da simulação.

## 🗺️ Roadmap (Melhorias Futuras)

* [ ] Melhorar o tratamento de exceções (Ex: ativo não encontrado, período sem dados).
* [ ] Adicionar novas estratégias (Ex: Índice de Força Relativa - IFR, Bandas de Bollinger).
* [ ] Implementar mais métricas de performance (Ex: Sharpe Ratio, Max Drawdown, comparação com Buy & Hold).

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Autor

* **Matheus Blanco Vitorino** - [LinkedIn](https://linkedin.com/in/matheus-vitorino-/)