#Rotina para criação do Dataset de Teor de Enxofre
#Organizar os dados em um único arquivo CSV, juntando os espectros e as propriedades (massa específica)

import os # para manipulação de caminhos de arquivos
import pandas as pd
import openpyxl 

# 1) Organização dos arquivos e pastas


nome_coluna_codigo = "codigo"                  # nome da coluna com o código da amostra
pasta_espectros = "CSV_Convertidos"  # pasta onde estão os arquivos CODIGO.csv

# 2) Ler o excel código + propriedade

# Usar o caminho do próprio script para abrir o arquivo no mesmo diretório
caminho_excel = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dados_enxofre.xlsx')
print('Lendo arquivo:', caminho_excel)
tabela_propriedades = pd.read_excel(caminho_excel)

# garantir que o código fique como texto
tabela_propriedades[nome_coluna_codigo] = tabela_propriedades[nome_coluna_codigo].astype(str)

# a lista de amostras a buscar 
amostras_selecionadas = tabela_propriedades[nome_coluna_codigo].tolist()

# 3) Para cada amostra selecionada, ler o espectro e guardar numa lista

lista_de_linhas = []  # cada item vai ser um dicionário representando uma amostra

for codigo in amostras_selecionadas:

    caminho_do_arquivo = os.path.join(pasta_espectros, codigo + ".csv")

    # se o arquivo não existir, avisa e pula essa amostra
    if not os.path.exists(caminho_do_arquivo):
        print("Aviso: não encontrei o espectro da amostra", codigo)
        continue

    # lê o espectro: tem cabeçalho (Wavenumber;Absorbance), separador é ; e decimal é ,
    espectro = pd.read_csv(caminho_do_arquivo, sep=";", decimal=",")
    comprimentos_de_onda = espectro["Wavenumber"]
    absorbancias = espectro["Absorbance"]

    # monta um dicionário: {codigo: ..., comprimento_onda_1: absorbancia_1, ...}
    linha = {nome_coluna_codigo: codigo}

    for comprimento, absorbancia in zip(comprimentos_de_onda, absorbancias):
        linha[comprimento] = absorbancia

    lista_de_linhas.append(linha)

# 4) Transformar a lista de espectros numa tabela

tabela_espectros = pd.DataFrame(lista_de_linhas)

# 5) Juntar a tabela de espectros com a tabela de propriedades

tabela_final = pd.merge(tabela_propriedades, tabela_espectros, on=nome_coluna_codigo, how="inner")

print("Tabela final montada com", tabela_final.shape[0], "amostras e", tabela_final.shape[1], "colunas")
print(tabela_final.head())

# Salvar o resultado em um novo csv
tabela_final.to_csv("tabela_combinada_enxofre.csv", index=False)