# Robô Mercado Livre

Este projeto automatiza a consulta de preços e coleta de informações de produtos no site do Mercado Livre, passando os dados relevantes para uma planilha Excel.

## Funcionalidades

1. Consulta de produtos no Mercado Livre.
2. Navegação por todas as páginas de resultados.
3. Coleta de valores, títulos e URLs dos produtos.
4. Ordenação dos produtos pelos três menores preços.
5. Download de imagens e informações dos produtos.
6. Exportação das informações para uma planilha Excel.

## Tecnologias Utilizadas

* [Python](https://www.python.org/) 3.12.4
* [Playwright](https://playwright.dev/python/) - Automação de navegadores web
* [Openpyxl](https://openpyxl.readthedocs.io/en/stable/) 3.1.5 - Manipulação de Planilhas Excel

## Pré-requisitos

Certifique-se de ter Python 3.12.4 e Playwright instalados na sua máquina.

## Instalação

1. Clone o repositório:
    ```sh
    git clone https://github.com/victor/robot-sac-carrier-notification
    ```
  
2. Crie um ambiente virtual:
    ```sh
    python -m venv venv
    ```

3. Ative o ambiente virtual:

    * No Windows:
        ```sh
        venv\Scripts\activate
        ```

    * No macOS/Linux:
        ```sh
        source venv/bin/activate
        ```

4. Instale as dependências:
    ```sh
    pip install -r requirements.txt
    ```

## Configuração

1. **Configuração do Playwright**: Verifique se o Playwright e outras bibliotecas estão instaladas corretamente.

## Uso/Exemplo

Para iniciar a coleta de dados e processamento, execute o seguinte comando:
```sh
python main.py
