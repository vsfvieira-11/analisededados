# Dashboard interativo do projeto

Esta aplicação em React + Vite foi criada para visualizar, de forma modular e interativa, os resultados do fluxo de análise do projeto para os conjuntos de Enxofre, Fulgor e Massa específica.

## O que a aplicação oferece

- Abas separadas para cada conjunto de dados:
  - Enxofre
  - Fulgor
  - Massa específica
- Gráficos interativos com Plotly para:
  - histograma das propriedades;
  - PCA (scores PC1 x PC2);
  - loadings do PCA;
  - boxplot da distribuição das propriedades;
- Tabela resumida com as primeiras amostras carregadas;
- Seção com os passos do fluxo de cada conjunto, mapeando os scripts do projeto.

## Estrutura do projeto

```text
frontend/
├── index.html
├── package.json
├── vite.config.js
├── src/
│   ├── App.jsx
│   ├── index.css
│   └── main.jsx
└── README.md
```

## Requisitos

Antes de rodar a aplicação, é necessário ter instalado:

- Node.js 18+ (recomendado LTS)
- npm

## Instalação

Na pasta do frontend, execute:

```bash
npm install
```

## Execução local

Inicie o servidor de desenvolvimento:

```bash
npm run dev
```

A aplicação ficará disponível em:

```text
http://localhost:3000/
```

## Build de produção

Para gerar a versão otimizada para publicação:

```bash
npm run build
```

Os arquivos prontos para distribuição serão gerados na pasta `dist/`.

## Como os dados são carregados

A aplicação lê arquivos CSV já presentes no projeto, em especial:

- `PCA/pca_dataset.csv`
- `resultados_pca/scores_pca.csv`
- `resultados_pca/loadings.csv`

Esses arquivos são usados para montar a interface, garantindo que todas as amostras disponíveis no conjunto sejam consideradas nos gráficos.

## Fluxo de uso

1. Abra a aplicação no navegador.
2. Selecione a aba correspondente ao conjunto desejado.
3. Escolha a métrica de interesse no seletor.
4. Analise os gráficos interativos e a tabela de amostras.
5. Use os cards de passos para acompanhar qual script do projeto corresponde a cada etapa do fluxo.

## Personalização

É possível expandir a aplicação facilmente para adicionar:

- gráficos de resíduos;
- gráficos de validação do modelo;
- filtros por amostra;
- comparação entre os três conjuntos em uma única visão;
- exportação de gráficos em imagem ou PDF.

## Observações importantes

- Os gráficos foram desenhados para serem interativos e responsivos.
- O projeto foi organizado de forma modular para facilitar manutenção futura.
- O dashboard foi pensado para servir como porta de entrada visual do fluxo analítico do projeto.
