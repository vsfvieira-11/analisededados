# 1. Importando as bibliotecas necessárias
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cross_decomposition import PLSRegression
from sklearn.model_selection import cross_val_predict, train_test_split, KFold
from sklearn.metrics import r2_score, mean_squared_error
import plotly.graph_objects as go

# 2. Carregaregando os dados da tabela combinada
tabela1 = pd.read_csv("tabela_combinada_massa_esp_sem_outliers.csv", index_col=0)

y = tabela1.iloc[:, 0]          
X = tabela1.iloc[:, 1:]         

nomes_variaveis = X.columns.tolist()  # nomes dos comprimentos de onda

# 3. Divisão dos dados em conjunto de treino e teste
X_train, X_test, y_train, y_test = train_test_split(
    X, 
    y, test_size=0.33, 
    random_state=7,
    shuffle=True
)

print("="*60)
print("DIVISÃO DOS DADOS")

print(f"Número total de amostras : {len(y)}")
print(f"Amostras de treinamento  : {len(y_train)}")
print(f"Amostras de teste        : {len(y_test)}")
print(f"Número de variáveis      : {X.shape[1]}")

# 4. Autoescalamento do dados em X 

scaler = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc = scaler.transform(X_test)

print("Médias (treino)")
print(scaler.mean_)

print("\nVariâncias (treino)")
print(scaler.var_)

print("\nVerificação - treino escalado")
print("Média:", X_train_sc.mean(axis=0)[:5])
print("Std:", X_train_sc.std(axis=0)[:5])

# 4.1 Definição do esquema de validação cruzada (KFold com shuffle)
# Importante: por padrão o cross_val_predict NÃO embaralha os dados antes
# de montar os folds. Se as amostras estiverem ordenadas no CSV (por data,
# lote, tipo de amostra etc.), os folds podem ficar não representativos,
# distorcendo RMSECV e Q². Por isso definimos um KFold explícito com
# shuffle=True e random_state fixo (reprodutibilidade).
cv_scheme = KFold(n_splits=5, shuffle=True, random_state=7)


# 5. Treinamento do modelo PLS final com o melhor número de LVs
# (use o número que você já encontrou na seleção de LVs)

best_lv = 8  # <-- ajuste aqui se necessário

pls_final = PLSRegression(n_components=best_lv)
pls_final.fit(X_train_sc, y_train)

# 6. Cálculo dos VIP Scores e in Projection)

def calcular_vip(modelo): #Calcula o VIP para cada variável (comprimento de onda) do modelo PLS.
    #Variáveis com VIP > 1 são consideradas importantes.
   
    T = modelo.x_scores_          # scores (amostras x LVs)
    W = modelo.x_weights_         # pesos  (variáveis x LVs)
    Q = modelo.y_loadings_        # loadings de Y (propriedade x LVs)

    n_variaveis = W.shape[0]
    n_lv = W.shape[1]

    variancia_explicada = np.diag(T.T @ T @ Q.T @ Q)
    variancia_total = np.sum(variancia_explicada)

    vip = np.sqrt(
        n_variaveis * np.sum(
            [(variancia_explicada[lv] / variancia_total) * (W[:, lv] / np.linalg.norm(W[:, lv])) ** 2
             for lv in range(n_lv)],
            axis=0
        )
    )
    return vip

vip = calcular_vip(pls_final)

print("="*60)
print("SELEÇÃO DE VARIÁVEIS POR VIP")
print(f"Total de variáveis: {len(vip)}")
print(f"Variáveis com VIP > 1: {np.sum(vip > 1)}")

# 7. Gráfico do VIP por comprimento de onda

comprimentos_de_onda = [int(float(c)) for c in nomes_variaveis]

fig_vip = go.Figure()

fig_vip.add_trace(go.Scatter(
    x=comprimentos_de_onda,
    y=vip,
    mode="lines",
    name="VIP"
))

fig_vip.add_hline(
    y=1,
    line_dash="dash",
    line_color="red",    
)

fig_vip.update_layout(
    title="VIP Scores por comprimento de onda - Massa Específica",
    xaxis_title="Comprimento de onda (nm)",
    yaxis_title="VIP Scores"
)

fig_vip.show()

# 8. Seleção de variáveis com VIP Scores > 1
variaveis_selecionadas = vip > 1
X_train_sel = X_train_sc[:, variaveis_selecionadas]
X_test_sel = X_test_sc[:, variaveis_selecionadas]

print(f"\nRe-treinando o modelo com {X_train_sel.shape[1]} variáveis selecionadas...")

# 9. Seleção do melhor número de LVs para o modelo reduzido
mse_cv_sel = []
max_lv_testar = min(20, X_train_sel.shape[1])

for i in range(max_lv_testar):
    modelo_sel = PLSRegression(n_components=i + 1)
    y_cv = cross_val_predict(modelo_sel, X_train_sel, y_train, cv=10)
    mse_cv_sel.append(mean_squared_error(y_train, y_cv))

best_lv_sel = int(np.argmin(mse_cv_sel) + 1)
rmsecv_sel = np.sqrt(min(mse_cv_sel))

print(f"Melhor número de LVs com variáveis selecionadas: {best_lv_sel}")
print(f"RMSECV mínimo: {rmsecv_sel:.4f}")

# 10. Treinamento do modelo final reduzido
pls_final_sel = PLSRegression(n_components=best_lv_sel)
pls_final_sel.fit(X_train_sel, y_train)

y_train_pred_sel = pls_final_sel.predict(X_train_sel).flatten()
y_test_pred_sel = pls_final_sel.predict(X_test_sel).flatten()

# 11. Métricas finais do modelo reduzido
r2_train_sel = r2_score(y_train, y_train_pred_sel)
rmsec_sel = np.sqrt(mean_squared_error(y_train, y_train_pred_sel))

r2_test_sel = r2_score(y_test, y_test_pred_sel)
rmsep_sel = np.sqrt(mean_squared_error(y_test, y_test_pred_sel))

y_cv_sel = cross_val_predict(pls_final_sel, X_train_sel, y_train, cv=10)
q2_sel = r2_score(y_train, y_cv_sel)

rmsep_rmsec_taxa_sel = rmsep_sel / rmsec_sel
rpdtreino_sel = np.std(y_train) / rmsec_sel
rpdtest_sel = np.std(y_test) / rmsep_sel

print("="*60)
print("MODELO FINAL PLS COM VARIÁVEIS SELECIONADAS (VIP > 1)")
print(f"Número de variáveis latentes (LVs): {best_lv_sel}")
print(f"Número de variáveis (comprimentos de onda): {X_train_sel.shape[1]}")
print(f"Amostras de treino: {len(y_train)}")
print(f"Amostras de teste: {len(y_test)}")
print("="*60)
print("MÉTRICAS FINAIS DO MODELO PLS REDUZIDO")

print(f"R² (treino) : {r2_train_sel:.3f}")
print(f"RMSEC       : {rmsec_sel:.3f}")

print("-"*60)

print(f"R² (teste)  : {r2_test_sel:.3f}")
print(f"RMSEP       : {rmsep_sel:.3f}")

print("-"*60)

print(f"Q² (CV)     : {q2_sel:.3f}")
print(f"RMSEP/RMSEC : {rmsep_rmsec_taxa_sel:.3f}")
print(f"RPD (treino): {rpdtreino_sel:.3f}")
print(f"RPD (teste) : {rpdtest_sel:.3f}")

# 12. Gráfico de dispersão: Valores medidos vs Valores previstos

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=np.array(y_train).flatten(),
    y=y_train_pred_sel,
    mode="markers",
    name="Treino",
    marker=dict(symbol="triangle-up", size=8)
))

fig.add_trace(go.Scatter(
    x=np.array(y_test).flatten(),
    y=y_test_pred_sel,
    mode="markers",
    name="Teste",
    marker=dict(symbol="circle", size=8)
))

y_all = np.concatenate([
    np.array(y_train).flatten(),
    np.array(y_test).flatten(),
    y_train_pred_sel,
    y_test_pred_sel
])

min_val = y_all.min()
max_val = y_all.max()

fig.add_trace(go.Scatter(
    x=[min_val, max_val],
    y=[min_val, max_val],
    mode="lines",
    line=dict(color="red", dash="dash"),
    name="Ideal (y = x)"
))

fig.update_layout(
    title="PLS Massa Específica (Variáveis Selecionadas-VIP) - Medido vs Previsto",
    xaxis_title="Valor medido (kg/m³)",
    yaxis_title="Valor previsto (kg/m³)"
)

fig.show()