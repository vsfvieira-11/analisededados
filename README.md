# Análise e visualização de espectros

Este projeto foi criado para organizar, converter e visualizar espectros em formato CSV, principalmente para análises FTIR/MIR. O fluxo principal é realizado em um notebook Jupyter chamado Conversor.ipynb e tem dois objetivos claros:

1. converter arquivos CSV com separador `;` e decimal `,` para um formato padronizado;
2. gerar um gráfico com todos os espectros tratados, permitindo uma inspeção visual rápida das amostras.

O código foi pensado para ser simples, transparente e fácil de adaptar para diferentes conjuntos de dados.

## O que o projeto faz

O notebook executa duas etapas:

- Conversão de arquivos brutos: lê arquivos CSV com estrutura específica, padroniza as colunas e salva uma versão tratada.
- Visualização dos espectros: lê os arquivos já tratados e plota todas as curvas em um único gráfico para comparação visual.

Essa abordagem é útil quando você precisa:

- preparar dados para análise posterior;
- padronizar o formato de entrada;
- inspecionar rapidamente a forma dos espectros;
- comparar várias amostras em um mesmo gráfico.

## Estrutura da pasta do projeto

```text
trabalho_final/
├── Conversor.ipynb
├── CSV_Convertidos/
├── Enxofre/
├── Espectros/
├── Fulgor/
├── Histograma/
├── Massa_esp/
├── PCA/
├── resultados_pca/
└── README.md
```

### Descrição das pastas

- CSV_Convertidos/: pasta usada para armazenar os arquivos já convertidos ou processados.
- Enxofre/, Fulgor/, Massa_esp/: pastas relacionadas a diferentes conjuntos ou tipos de análises.
- Espectros/: local provável para armazenar ou organizar espectros.
- Histograma/, PCA/, resultados_pca/: pastas usadas para análises complementares e resultados.

## Requisitos

Antes de executar o notebook, é necessário ter instalado:

- Python 3.9 ou superior
- Jupyter Notebook ou JupyterLab
- Bibliotecas Python:
  - pandas
  - matplotlib

Você pode instalar as dependências com:

```bash
pip install pandas matplotlib jupyter
```

## Como usar o projeto

### 1. Organize os arquivos de entrada

Os arquivos de entrada devem estar em uma pasta acessível ao notebook. O primeiro bloco do código procura por arquivos com extensão `.csv` ou `.CSV` em uma pasta definida por `pasta_csv`.

Para o fluxo funcionar corretamente, os arquivos devem:

- estar em formato CSV;
- estar salvos com a estrutura esperada pela leitura;
- possuir separador `;` e decimal `,` no caso da conversão inicial.

### 2. Execute a célula de conversão

A primeira parte do notebook realiza a conversão. Ela lê cada arquivo, troca o separador e padroniza as colunas para:

- `Numero_Onda`
- `Absorbancia`

Depois, salva o arquivo com o mesmo nome base, sobrescrevendo a versão original na pasta de destino.

### 3. Execute a célula de visualização

A segunda parte do notebook lê os arquivos tratados com o padrão `_tratado.csv` e gera um gráfico com todos os espectros.

## Explicação detalhada dos parâmetros

A seguir, cada parâmetro importante do código é explicado de forma prática.

### 1. `pasta_csv` (primeira célula)

```python
pasta_csv = 'CSV'
```

Este parâmetro define a pasta onde os arquivos CSV serão procurados.

O que fazer:

- use uma pasta real e existente no seu computador;
- se a pasta tiver outro nome, troque o valor para o caminho correto;
- se você quiser salvar os arquivos convertidos em outra pasta, ajuste esse valor.

Importante:

- no notebook atual, a pasta usada está configurada de forma simples e pode precisar de ajuste conforme o ambiente em que você estiver executando.

### 2. `glob.glob(os.path.join(pasta_csv, "*.csv"))`

Esta instrução procura arquivos com extensão `.csv` dentro da pasta definida.

O que ela faz:

- encontra todos os arquivos com esse formato;
- permite que o código processe vários arquivos automaticamente.

Se quiser incluir outros formatos, é possível ajustar o padrão.

### 3. `glob.glob(os.path.join(pasta_csv, "*.CSV"))`

É a mesma ideia do item anterior, mas para arquivos com extensão `.CSV` em maiúsculas.

Por que isso é útil:

- alguns arquivos exportados por programas diferentes podem vir com letras maiúsculas;
- isso evita falhas na leitura por causa da extensão.

### 4. `sep=";"`

```python
df = pd.read_csv(arquivo, sep=";", decimal=",")
```

Este parâmetro informa ao pandas que o arquivo de entrada usa ponto e vírgula como separador de colunas.

Quando usar:

- se o CSV foi exportado com esse formato;
- se os dados vierem em colunas organizadas por `;`.

Se o seu arquivo estiver usando vírgula em vez de ponto e vírgula, o código vai ler de forma incorreta.

### 5. `decimal=","`

Este parâmetro informa que o separador decimal do arquivo é a vírgula, e não o ponto.

Exemplo:

- valor correto no arquivo: `1,234`
- se o código não usar `decimal=","`, o pandas pode interpretar isso de forma errada.

### 6. `df.columns = ["Numero_Onda", "Absorbancia"]`

Aqui o código padroniza os nomes das colunas para dois nomes fixos.

Por que isso é importante:

- facilita a leitura posterior;
- evita erro quando outras partes do fluxo esperam esses nomes;
- torna o projeto mais consistente.

### 7. `nome_saida = os.path.join(...)`

Este trecho define o nome do arquivo de saída.

Ele usa:

- o nome original do arquivo;
- a extensão `.csv`;
- a pasta definida em `pasta_csv`.

Ou seja, o código salva a versão convertida mantendo quase o mesmo nome do arquivo original.

### 8. `df.to_csv(nome_saida, index=False)`

Esse comando grava o DataFrame em um novo arquivo CSV sem incluir a coluna de índice do pandas.

Por que isso é vantajoso:

- o arquivo fica mais limpo;
- é compatível com a maioria das ferramentas de análise;
- reduz ruído desnecessário no resultado final.

### 9. `pasta_csv` (segunda célula)

Na segunda parte do notebook, existe um outro valor de `pasta_csv`:

```python
pasta_csv = r"C:\Users\marcu\OneDrive\Área de Trabalho\CSV"
```

Esse parâmetro define onde os arquivos já tratados serão procurados para plotagem.

Atenção:

- esse caminho está fixado para um computador específico;
- em seu ambiente, ele provavelmente precisa ser alterado para o caminho correto da sua máquina.

Se o caminho estiver incorreto, o gráfico não será gerado corretamente ou o notebook não encontrará arquivos.

### 10. `glob.glob(os.path.join(pasta_csv, "*_tratado.csv"))`

Esta instrução procura apenas arquivos cujo nome termina com `_tratado.csv`.

Isso é importante porque:

- o código assume que os arquivos plotados já foram processados;
- ele não tenta plotar arquivos brutos ou incompatíveis.

Se os seus arquivos tiverem outro padrão de nome, ajuste essa parte.

### 11. `linewidth=0.5` e `alpha=0.4`

Esses parâmetros controlam a aparência das linhas no gráfico.

- `linewidth`: espessura da linha;
- `alpha`: transparência.

Eles ajudam a visualizar sobreposição de curvas sem deixar o gráfico excessivamente carregado.

### 12. `plt.gca().invert_xaxis()`

Essa linha inverte o eixo x.

Por que isso pode ser útil:

- em espectros, a ordem das ondas costuma ser apresentada em ordem decrescente;
- inverter o eixo melhora a leitura visual e torna o gráfico mais intuitivo.

### 13. `plt.xlabel`, `plt.ylabel`, `plt.title`

Esses parâmetros definem os rótulos do gráfico.

- eixo x: número de onda em cm⁻¹;
- eixo y: absorbância;
- título: descrição visual do conjunto de espectros.

## O que fazer para tirar o melhor proveito do código

### 1. Verifique o formato real dos arquivos

Antes de executar a conversão, abra alguns arquivos para confirmar:

- se o separador é `;`;
- se o decimal é `,`;
- se as colunas têm a ordem esperada;
- se existem linhas vazias ou dados corrompidos.

### 2. Use nomes consistentes

Se possível, mantenha um padrão de nomenclatura para os arquivos, por exemplo:

- `amostra_01.csv`
- `amostra_02.csv`
- `amostra_03_tratado.csv`

Isso facilita a automação e evita confusão na hora de plotar.

### 3. Ajuste os caminhos manualmente

O notebook tem um caminho fixo para a pasta de leitura na segunda parte. Em seu computador, esse valor deve ser alterado para a pasta correta.

### 4. Revise os arquivos convertidos

Depois da conversão, abra alguns arquivos gerados para confirmar se:

- as colunas foram renomeadas corretamente;
- não houve perda de dados;
- o arquivo ficou legível e consistente.

### 5. Use o gráfico como ferramenta de diagnóstico

O gráfico de espectros é excelente para identificar:

- amostras com ruído excessivo;
- arquivos mal formatados;
- diferenças de intensidade entre amostras;
- padrões que merecem análise posterior.

### 6. Mantenha backups

Como o notebook salva arquivos na pasta de trabalho, vale a pena:

- manter uma cópia dos arquivos originais;
- revisar os resultados antes de sobrescrever arquivos importantes.

## Fluxo recomendado

1. Coloque os arquivos CSV na pasta de entrada.
2. Ajuste `pasta_csv` para o diretório correto.
3. Execute a célula de conversão.
4. Confirme se os arquivos foram salvos corretamente.
5. Ajuste o caminho da segunda célula para a pasta com os arquivos tratados.
6. Execute a célula de visualização.
7. Analise o gráfico gerado e revise eventuais inconsistências.

## Dicas adicionais

- Se o seu arquivo não estiver sendo lido corretamente, verifique o separador e o decimal.
- Se o gráfico estiver vazio, confirme se os arquivos realmente existem na pasta indicada.
- Se você quiser ampliar o projeto, pode incluir filtros, normalização de intensidade, ou análise estatística dos espectros.

## Resumo

Este projeto é um fluxo simples, mas útil, para:

- transformar arquivos CSV brutos em dados padronizados;
- preparar espectros para análise;
- visualizar várias curvas de forma comparativa.

Com pequenas adaptações nos caminhos e nos parâmetros, ele pode ser usado de forma eficiente para diferentes bases de dados e diferentes tipos de análise espectral.
