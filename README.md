# Análise e visualização de espectros

Este projeto foi criado para organizar, converter e visualizar espectros em formato CSV, principalmente para análises FTIR/MIR. O fluxo principal é realizado em um notebook Jupyter chamado Conversor.ipynb e tem dois objetivos claros:

1. converter arquivos CSV com separador `;` e decimal `,` para um formato padronizado;
2. gerar um gráfico com todos os espectros tratados, permitindo uma inspeção visual rápida das amostras.

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
- Espectros/: local para armazenar os espectros em .SPA.
- Histograma/, PCA/, resultados_pca/: pastas usadas para análises complementares e resultados.

## Requisitos

Antes de executar o notebook, é necessário ter instalado:

- Python 3.9 ou superior
- Jupyter Notebook ou JupyterLab
- Bibliotecas Python:
  - pandas
  - matplotlib
  - os
  - numpy
  - plotly
  - scikit-learn

Você pode instalar as dependências com:

```bash
pip install pandas matplotlib jupyter os numpy plotly scikit-learn
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

### 3. Obtenção de modelos

Em cada diretório de cada ensaio físico-químico (Enxofre, Ponto de Fulgor e Massa Específica) é encontrado a mesma estrutura.

Devem ser executados na seguinte ordem:
- data_*.py
- modelo_*.py
- modelo_*_soutliers.py
- calculo_residuos_*.py
- data_*_VIP_soutlier.py

### 4. Histogramas

Para obter os histogramas de cada ensaio físico-químico (Enxofre, Ponto de Fulgor e Massa Específica) deve se dirigir ao diretório "Hisograma" e rodar o programa "Histograma_amostras.py". Será gerado os 3 histogramas.

### 5. PCA

Para obter o PCA de cada ensaio físico-químico (Enxofre, Ponto de Fulgor e Massa Específica) deve se dirigir ao diretório "PCA" e rodar o programa "PCA.py". Os resultados serão gerados no diretório "resultados_pca".