# 1. Importando as bibliotecas necessárias
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_predict
from sklearn.cross_decomposition import PLSRegression
from sklearn.metrics import r2_score, mean_squared_error
import plotly.graph_objects as go

# 2. Carregando os dados da tabela combinada
tabela1 = pd.read_csv("tabela_combinada_enxofre.csv", index_col=0)

Y = tabela1.iloc[:, [0]]   # coluna da propriedade
X = tabela1.iloc[:, 1:]    # colunas dos espectros

# 3. Divisão dos dados em conjunto de treino e teste
X_train, X_test, y_train, y_test = train_test_split(
    X,
    Y,
    test_size=0.33,
    random_state=42,
    shuffle=True
)

# 4. Autoescalamento dos dados em X
scaler = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc = scaler.transform(X_test)

# 5. Seleção do número de variáveis latentes
max_comp = 20
rmsecv_list = []

for n_comp in range(1, max_comp + 1):
    pls = PLSRegression(n_components=n_comp)
    pls.fit(X_train_sc, y_train)
    y_cv = cross_val_predict(pls, X_train_sc, y_train, cv=10)
    rmsecv_list.append(np.sqrt(mean_squared_error(y_train, y_cv)))

best_lv = np.argmin(rmsecv_list) + 1
print(f"Melhor número de LVs: {best_lv}")
print(f"RMSECV mínimo: {rmsecv_list[best_lv-1]:.4f}")

# 6. Modelo final ajustado com o melhor número de variáveis latentes
pls_final = PLSRegression(n_components=best_lv)
pls_final.fit(X_train_sc, y_train)

# 7. Previsão do conjunto de treino e teste
y_train_pred = pls_final.predict(X_train_sc).flatten()
y_test_pred = pls_final.predict(X_test_sc).flatten()

# 8. Calcular resíduos e limite de outliers (2 desvios padrão)
residuos_treino = np.array(y_train).flatten() - y_train_pred
residuos_teste = np.array(y_test).flatten() - y_test_pred
residuos_todos = np.concatenate([residuos_treino, residuos_teste])

limite = 2 * np.std(residuos_todos)

print("="*60)
print("DETECÇÃO DE OUTLIERS POR RESÍDUO")
print(f"Limite (2 desvios padrão): ± {limite:.4f}")
print(f"Amostras totais          : {len(residuos_todos)}")
print(f"Amostras removidas       : {np.sum(np.abs(residuos_todos) > limite)}")
print(f"Amostras restantes       : {np.sum(np.abs(residuos_todos) <= limite)}")

# 9. Gráfico de resíduos
fig_residuos = go.Figure()

fig_residuos.add_trace(go.Scatter(
    x=np.array(y_train).flatten(),
    y=residuos_treino,
    mode="markers",
    name="Treino",
    marker=dict(symbol="triangle-up", size=8)
))

fig_residuos.add_trace(go.Scatter(
    x=np.array(y_test).flatten(),
    y=residuos_teste,
    mode="markers",
    name="Teste",
    marker=dict(symbol="circle", size=8)
))

# linha de resíduo zero
fig_residuos.add_hline(
    y=0,
    line_dash="dash",
    line_color="red",
    annotation_text="Resíduo = 0"
)

# linhas de +2 e -2 desvios padrão
fig_residuos.add_hline(
    y=limite,
    line_dash="dot",
    line_color="gray",
    annotation_text="+2 dp"
)

fig_residuos.add_hline(
    y=-limite,
    line_dash="dot",
    line_color="gray",
    annotation_text="-2 dp"
)

fig_residuos.update_layout(
    title="Gráfico de Resíduos — PLS Enxofre (Dados Brutos)",
    xaxis_title="Valor medido (mg/kg)",
    yaxis_title="Resíduo (medido - previsto)"
)

fig_residuos.show()

# 10. Salvar tabela sem outliers
indices_ok = np.concatenate([
    X_train.index[np.abs(residuos_treino) <= limite],
    X_test.index[np.abs(residuos_teste) <= limite]
])

tabela_sem_outliers = tabela1.loc[indices_ok]
tabela_sem_outliers.to_csv("tabela_combinada_enxofre_sem_outliers.csv")

print(f"\nArquivo salvo: tabela_combinada_enxofre_sem_outliers.csv")
print(f"Total de amostras no novo arquivo: {len(tabela_sem_outliers)}")