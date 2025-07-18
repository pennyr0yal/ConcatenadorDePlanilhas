# Concatenador de Planilhas
Este programa permite ao usuário **selecionar múltiplos arquivos** de uma pasta (com suporte a `.xlsx` e `.csv`) por meio de uma **interface gráfica interativa**. Os arquivos selecionados são lidos e concatenados em um único arquivo chamado `saida.csv`.

---

## Funcionalidades

- Usuário seleciona a pasta via janela do sistema.
- Arquivos da pasta são listados e o usuário escolhe entre concatenar todas ou selecionar arquivos específicos. Inclui campo de busca para filtrar arquivos pelo nome.
- Programa automaticamente lê os formatos:
  - `.csv` (separador `;` ou `,`)
  - `.xlsx`
- Dados são concatenados e exportados para `saida.xlsx`;
- Exibe avisos em caso de erros de leitura ou formatos não suportados;

## Como Usar

1. Execute o arquivo .bat na pasta principal. O programa instalará o venv e as bibliotecas necessárias.
2. Uma janela irá abrir, selecione a **pasta com os arquivos** desejados. O repositório inclui uma pasta "Arquivos" para testes.
3. Use os checkboxes ou o campo de busca para escolher os arquivos a serem concatenados.
4. Clique em **OK** para iniciar a leitura e concatenação.
5. O resultado será salvo no mesmo diretório como `saida.xlsx`.

## Formatos Suportados

| Extensão | Método de Leitura |
|----------|-------------------|
| `.csv`   | `pandas.read_csv()` com `sep=';'` ou `sep=','` |
| `.xlsx`  | `pandas.read_excel()` |

## Observações

- A interface foi desenvolvida com `tkinter`.
- Arquivos com extensões não suportadas serão **ignorados** e listados em um aviso após a execução.
- O programa suporta apenas planilhas com os mesmos headers. Uma melhoria possível é detectar e alertar o usuário sobre diferenças entre os arquivos selecionados e permitir uma comparação entre as colunas existentes.

# Autora
Desenvolvido por Natalia Junghans

📧 natbjunghans@gmail.com
