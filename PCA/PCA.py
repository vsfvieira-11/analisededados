#PCA usando apenas as propriedades físico-químicas: massa específica, ponto de fulgor, enxofre(gráficos interativos com Plotly)

#Importando bibliotecas
import os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

os.makedirs("resultados_pca", exist_ok=True) #criando uma pasta no diretório atual para salvar os resultados

# 1. CONFIGURAÇÃO
CAMINHO_ARQUIVO = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pca_dataset.csv')  # caminho do arquivo CSV com os dados

COLUNA_ID = "amostra"                # coluna de ID da amostra

COLUNAS_PROPRIEDADES = [
    "ponto de fulgor",
    "massa especifica",
    "enxofre",
]

# 2. CARREGAMENTO DO DADOS
if CAMINHO_ARQUIVO.endswith(".csv"):
    # separador ";" e decimal "," (padrão BR)
    df = pd.read_csv(CAMINHO_ARQUIVO, sep=";", decimal=",")
else:
    df = pd.read_excel(CAMINHO_ARQUIVO)

print(f"Dimensão dos dados: {df.shape}")
print(df.head())

if COLUNA_ID and COLUNA_ID in df.columns:
    ids = df[COLUNA_ID].astype(str).values
else:
    ids = df.index.astype(str).values


# 3. MATRIZ DE DADOS (apenas as 3 propriedades)
X = df[COLUNAS_PROPRIEDADES].values

# 4. PADRONIZAÇÃO
scaler = StandardScaler() #Autoescalamento (padronização) dos dados: média=0, desvio padrão=1
X_scaled = scaler.fit_transform(X)


# 5. PCA
pca = PCA()  # com 3 variáveis, no máximo 3 componentes
scores = pca.fit_transform(X_scaled)

n_comp = X_scaled.shape[1]
nomes_pc = [f"PC{i+1}" for i in range(n_comp)]
var_explicada = pca.explained_variance_ratio_ * 100
var_acumulada = np.cumsum(var_explicada)

print("\n=== Variância explicada por componente ===")
for i, (v, va) in enumerate(zip(var_explicada, var_acumulada), start=1):
    print(f"PC{i}: {v:.2f}%  (acumulada: {va:.2f}%)")

# DataFrame de scores, já juntando ids e propriedades originais
scores_df = pd.DataFrame(scores, columns=nomes_pc)
scores_df.insert(0, "amostra", ids)
for prop in COLUNAS_PROPRIEDADES:
    scores_df[prop] = df[prop].values

# 6. GERAÇÃO DOS GRÁFICOS

fig_scree = go.Figure()
fig_scree.add_trace(go.Scatter(
    x=nomes_pc, y=var_explicada, mode="lines+markers", name="Individual"
))
fig_scree.add_trace(go.Scatter(
    x=nomes_pc, y=var_acumulada, mode="lines+markers", name="Acumulada",
    line=dict(dash="dash")
))
fig_scree.update_layout(
    title="Scree Plot",
    xaxis_title="Componente Principal",
    yaxis_title="Variância explicada (%)",
    template="plotly_white",
)
fig_scree.write_html("resultados_pca/scree_plot.html")

# 7. GRÁFICO DE SCORES (PC1 x PC2), colorido por cada propriedade
for prop in COLUNAS_PROPRIEDADES:
    fig_scores = px.scatter(
        scores_df, x="PC1", y="PC2",
        color=prop,
        hover_data=["amostra"] + COLUNAS_PROPRIEDADES,
        color_continuous_scale="Viridis",
        title=f"Scores PC1 x PC2 - colorido por {prop}",
        labels={
            "PC1": f"PC1 ({var_explicada[0]:.1f}%)",
            "PC2": f"PC2 ({var_explicada[1]:.1f}%)",
        },
    )
    fig_scores.add_hline(y=0, line_color="gray", line_width=0.5)
    fig_scores.add_vline(x=0, line_color="gray", line_width=0.5)
    fig_scores.update_layout(template="plotly_white")
    fig_scores.write_html(f"resultados_pca/scores_colorido_{prop}.html")

# Versão simples sem cor (só as amostras)
fig_scores_simple = px.scatter(
    scores_df, x="PC1", y="PC2",
    hover_data=["amostra"] + COLUNAS_PROPRIEDADES,
    title="Scores PC1 x PC2",
    labels={
        "PC1": f"PC1 ({var_explicada[0]:.1f}%)",
        "PC2": f"PC2 ({var_explicada[1]:.1f}%)",
    },
)
fig_scores_simple.add_hline(y=0, line_color="gray", line_width=0.5)
fig_scores_simple.add_vline(x=0, line_color="gray", line_width=0.5)
fig_scores_simple.update_layout(template="plotly_white")
fig_scores_simple.write_html("resultados_pca/scores_pc1_pc2.html")


# 8. LOADINGS
loadings = pd.DataFrame(
    pca.components_.T,
    columns=nomes_pc,
    index=COLUNAS_PROPRIEDADES,
)
print("\n=== Loadings ===")
print(loadings)
loadings.to_csv("resultados_pca/loadings.csv")


# 10. SALVAR SCORES EM CSV
scores_df.to_csv("resultados_pca/scores_pca.csv", index=False)

print("\nConcluído! Arquivos salvos em resultados_pca/:")
print("- scree_plot.html")
print("- scores_pc1_pc2.html")
print("- scores_colorido_<propriedade>.html (uma por propriedade)")
print("- biplot.html")
print("- loadings.csv")
print("- scores_pca.csv")