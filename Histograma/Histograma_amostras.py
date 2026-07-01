#HISTOGRAMA DOS DADOS PARA AVALIAÇÃO DO BANCO DE DADOS QUE SERÁ UTILIZADO

#MASSA ESPECÍFICA
import os
import pandas as pd
import plotly.express as px

# Carregar dados
caminho_excel = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'massa_esp.xlsx')
tabela_propriedades = pd.read_excel(caminho_excel)
df = pd.read_excel(caminho_excel)

# Criar histograma
fig = px.histogram(
    df,
    x='densidade',
    title='Histograma dos Dados de Massa Específica para Amostras de Diesel'
)

# Configuração das classes
fig.update_traces(
    xbins=dict(
        start=833.3,
        end=866,
        size=5.5
    ),
    marker_color='#BFD7EA',
    marker_line_color='black',
    marker_line_width=0.5
)

# Layout
fig.update_layout(
    template='simple_white',
    width=900,
    height=550,
    bargap=0,
    title_x=0.5,
    xaxis_title='Massa Específica (kg/m³)',
    yaxis_title='Frequência',
    font=dict(
        family='Arial',
        size=14
    )
)

# Escala do eixo X
fig.update_xaxes(
    range=[830, 870],
    tick0=830,
    dtick=5,
    showline=True,
    linewidth=1,
    linecolor='black',
    mirror=True
)

# Escala do eixo Y
fig.update_yaxes(
    tick0=0,
    dtick=5,
    showline=True,
    linewidth=1,
    linecolor='black',
    mirror=True
)

# Exibir gráfico
fig.show()

# Salvar gráfico
fig.write_html("histograma_massa_esp.html")


#TEOR DE ENXOFRE

import pandas as pd
import plotly.express as px

# Carregar dados

caminho_excel = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'enxofre.xlsx')
tabela_propriedades = pd.read_excel(caminho_excel)
df = pd.read_excel(caminho_excel)

# Criar histograma
fig = px.histogram(
    df,
    x='enxofre',
    title='Histograma dos Dados de Teor de Enxofre para Amostras de Diesel'
)

# Configuração das classes
fig.update_traces(
    xbins=dict(
        start=3.4,
        end=400,
        size=60
    ),
    marker_color='#BFD7EA',
    marker_line_color='black',
    marker_line_width=0.5
)

# Layout
fig.update_layout(
    template='simple_white',
    width=900,
    height=550,
    bargap=0,
    title_x=0.5,
    xaxis_title='Teor de Enxofre (mg/kg)',
    yaxis_title='Frequência',
    font=dict(
        family='Arial',
        size=14
    )
)

# Escala do eixo X
fig.update_xaxes(
    range=[0, 430],
    tick0=0,
    dtick=50,
    showline=True,
    linewidth=1,
    linecolor='black',
    mirror=True
)

# Escala do eixo Y
fig.update_yaxes(
    tick0=0,
    dtick=5,
    showline=True,
    linewidth=1,
    linecolor='black',
    mirror=True
)

# Exibir gráfico
fig.show()

# Salvar gráfico
fig.write_html("histograma_enxofre.html")

#TEOR DE PONTO DE FULGOR

import pandas as pd
import plotly.express as px

# Carregar dados
caminho_excel = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fulgor.xlsx')
tabela_propriedades = pd.read_excel(caminho_excel)
df = pd.read_excel(caminho_excel)

# Criar histograma
fig = px.histogram(
    df,
    x='fulgor',
    title='Histograma dos Dados de Ponto de Fulgor para Amostras de Diesel'
)

# Configuração das classes
fig.update_traces(
    xbins=dict(
        start=20,
        end=65,
        size=7
    ),
    marker_color='#BFD7EA',
    marker_line_color='black',
    marker_line_width=0.5
)

# Layout
fig.update_layout(
    template='simple_white',
    width=900,
    height=550,
    bargap=0,
    title_x=0.5,
    xaxis_title='Ponto de Fulgor (°C)',
    yaxis_title='Frequência',
    font=dict(
        family='Arial',
        size=14
    )
)

# Escala do eixo X
fig.update_xaxes(
    range=[20, 65],
    tick0=20,
    dtick=5,
    showline=True,
    linewidth=1,
    linecolor='black',
    mirror=True
)

# Escala do eixo Y
fig.update_yaxes(
    tick0=0,
    dtick=5,
    showline=True,
    linewidth=1,
    linecolor='black',
    mirror=True
)

# Exibir gráfico
fig.show()

# Salvar gráfico
fig.write_html("histograma_fulgor.html")
