#Rotina para criação de um modelo PLS para previsão da massa específica a partir dos espectros

# 1. Importando as bibliotecas necessárias
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_predict, KFold
from sklearn.cross_decomposition import PLSRegression
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
import plotly.graph_objects as go

# 2.Carregando os dados da tabela combinada
tabela1 = pd.read_csv("tabela_combinada_massa_esp.csv",index_col=0)
Y=tabela1.iloc[:,[0]] #selecionando a coluna da propriedade
print("Dimensões de Y")
print(Y.shape)

X = tabela1.iloc[:,1:] #selecionando as colunas dos espectros
print("Dimensões de X")
print(X.shape)

# 3. Divisão dos dados em conjunto de treino e teste
# Divisão: 67% treinamento e 33% teste
X_train, X_test, y_train, y_test = train_test_split(
    X,
    Y,
    test_size=0.33, # tamanho do conjunto de teste (33% dos dados)
    random_state=7, #manter a mesma divisão em diferentes execuções para que o código seja reprodutível para testes
    shuffle=True #embaralhamento aleatório dos dados antes da divisão
)

print("="*60)
print("DIVISÃO DOS DADOS")

print(f"Número total de amostras : {len(Y)}")
print(f"Amostras de treinamento  : {len(y_train)}")
print(f"Amostras de teste        : {len(y_test)}")
print(f"Número de variáveis      : {X.shape[1]}")

# 4. Autoescalamento dos dados em X

scaler = StandardScaler()

X_train_sc = scaler.fit_transform(X_train) # ajusta e transforma o conjunto de treinamento

X_test_sc = scaler.transform(X_test) # ajusta o conjunto de teste

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

# 5. Seleção do número de variáveis latentes

max_comp = 20

rmsecv = []
rmsec = []
r2_cv = []
r2_c = []

for n_comp in range(1, max_comp + 1):

    # modelo PLS
    pls = PLSRegression(n_components=n_comp)

    # ajusta no treino
    pls.fit(X_train_sc, y_train)

    # previsão no treino
    y_train_pred = pls.predict(X_train_sc)

    # validação cruzada no treino (usando o KFold com shuffle)
    y_cv = cross_val_predict(pls, X_train_sc, y_train, cv=cv_scheme)

    # métricas
    rmsec.append(np.sqrt(mean_squared_error(y_train, y_train_pred)))
    rmsecv.append(np.sqrt(mean_squared_error(y_train, y_cv)))
    r2_c.append(r2_score(y_train, y_train_pred))
    r2_cv.append(r2_score(y_train, y_cv))

# 6. Determinação do melhor número de variáveis latentes com base no RMSECV

best_lv = np.argmin(rmsecv) + 1 #retornar o índice do menor valor de RMSECV 

print("="*50)
print("SELEÇÃO DE VARIÁVEIS LATENTES")

print(f"Melhor número de LVs: {best_lv}")
print(f"RMSECV mínimo: {rmsecv[best_lv-1]:.4f}")

# 7. Gráficos de RMSEC e RMSECV
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=list(range(1, max_comp+1)),
    y=rmsec,
    mode="lines+markers",
    name="RMSEC"
))

fig.add_trace(go.Scatter(
    x=list(range(1, max_comp+1)),
    y=rmsecv,
    mode="lines+markers",
    name="RMSECV"
))

fig.update_layout(
    title="Seleção do número de Variáveis Latentes",
    xaxis_title="Número de Variáveis Latentes (VL)",
    yaxis_title="Raiz do Erro Quadrático Médio ",
)

fig.show()

# 6. Modelo final ajustado com o melhor número de variáveis latentes

pls_final = PLSRegression(n_components=best_lv) # Modelo final com o número ótimo de variáveis latentes
pls_final.fit(X_train_sc, y_train)# Ajuste do modelo SOMENTE com o conjunto de treino


# 7.Previsão do conjunto de treino e teste

y_train_pred = pls_final.predict(X_train_sc) # Previsão no treino

y_test_pred = pls_final.predict(X_test_sc) # Previsão no teste (validação externa)


#8. Organização dos Resultados

# garantir formato 1D
y_train_pred = y_train_pred.flatten()
y_test_pred = y_test_pred.flatten()

print("="*60)
print("MODELO FINAL PLS AJUSTADO")
print(f"Número de variáveis latentes (LVs): {best_lv}")
print(f"Amostras de treino: {len(y_train)}")
print(f"Amostras de teste: {len(y_test)}")


# 9. Métricas de desempenho do modelo final

# TREINO
r2_train = r2_score(y_train, y_train_pred)
rmsec = np.sqrt(mean_squared_error(y_train, y_train_pred))

# TESTE
r2_test = r2_score(y_test, y_test_pred)
rmsep = np.sqrt(mean_squared_error(y_test, y_test_pred))

## Q² (validação cruzada no treino, mesmo esquema KFold com shuffle)
y_cv = cross_val_predict(
    pls_final,
    X_train_sc,
    y_train,
    cv=cv_scheme
)

q2 = r2_score(y_train, y_cv)
rmsecv_final = np.sqrt(mean_squared_error(y_train, y_cv))

#RMSEP/RMSEC
rmsep_rmsec_taxa = rmsep / rmsec

# RPD 
rpdtreino = (np.std(y_train) / rmsec)
rpdtest = np.std(y_test) / rmsep

#Resultados finais
print("="*60)
print("MÉTRICAS FINAIS DO MODELO PLS")

print(f"R² (treino) : {r2_train:.3f}")
print(f"RMSEC       : {rmsec:.3f}")

print("-"*60)

print(f"R² (teste)  : {r2_test:.3f}")
print(f"RMSEP       : {rmsep:.3f}")

print("-"*60)

print(f"Q² (CV)       : {q2:.3f}")
print(f"RMSECV (final): {rmsecv_final:.3f}")
print(f"RMSEP/RMSEC   : {rmsep_rmsec_taxa:.3f}")
print(f"RPD (treino)  : {rpdtreino:.3f}")
print(f"RPD (teste)   : {rpdtest:.3f}")

# 10. Gráfico de dispersão: Valores medidos vs Valores previstos

fig = go.Figure()

fig.add_trace(go.Scatter( #conjunto de treinamento (triângulos)
    x=np.array(y_train).flatten(),
    y=np.array(y_train_pred).flatten(),
    mode="markers",
    name="Treino",
    marker=dict(symbol="triangle-up", size=8)
))

fig.add_trace(go.Scatter( #conjunto de teste (círculos)
    x=np.array(y_test).flatten(),
    y=np.array(y_test_pred).flatten(),
    mode="markers",
    name="Teste",
    marker=dict(symbol="circle", size=8)
))

y_all = np.concatenate([ #regressão de todos os valores (treino + teste)
    np.array(y_train).flatten(),
    np.array(y_test).flatten(),
    np.array(y_train_pred).flatten(),
    np.array(y_test_pred).flatten()
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

fig.update_layout( #dados do gráfico
    title="PLS para Determinação da Massa Específica em amostras de Diesel - Medido vs Previsto (Dados Brutos)",
    xaxis_title="Valor medido (kg/m³)",
    yaxis_title="Valor previsto (kg/m³)"
)

fig.show()