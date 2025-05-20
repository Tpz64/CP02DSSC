import streamlit as st
import pandas as pd
import time 
import plotly.express as px
import numpy as np
import statsmodels.api as sm
import plotly.graph_objects as go

#info lateral da equipe
st.sidebar.markdown("""
    <div style="
        background-color: #fffbf5; 
        color:white;
        padding: 9px; 
        border-radius: 10px;
        text-align: center;
    ">
        <p style="color:black; font-weight:bold;">Desenvolvido por:</p>
        <div>
            <a href="https://www.linkedin.com/in/andr%C3%A9-neves-2980b0270/" target="_blank" 
               style="color: black; text-decoration: none;">
                André de Sousa Neves
            </a>
        </div>
        <div>
            <a href="https://www.linkedin.com/in/becinaayu" target="_blank" 
               style="color: black; text-decoration: none;">
                Beatriz Dantas Sampaio
            </a>
        </div>
        <div>
            <a href="https://www.linkedin.com/in/isabela-barcellos-freire-91263328a/" target="_blank" 
               style="color: black; text-decoration: none;">
                Isabela Barcellos Freire
            </a>
        </div>
        <div>
            <a href="https://www.linkedin.com/in/thaisgleoncio/" target="_blank" 
               style="color: black; text-decoration: none;">
                Thaís Gonçalves Leoncio
            </a>
        </div>
    </div>
""", unsafe_allow_html=True)

st.header("Regressão Linear")

#Barra de carregamento
my_bar = st.progress(0)
for percent_complete in range(100):
     time.sleep(0.05)
     my_bar.progress(percent_complete + 1)

st.markdown("""
A regressão linear é uma técnica estatística usada para analisar a relação entre duas variáveis numéricas. O objetivo principal é prever o valor de uma variável (variável dependete, ou Y) a partir do valor de outra (variável independente, ou X).
No contexto desta análise, queremos saber se a produtividade do ajudante está relacionada à do eletricista, considerando apenas os casos em que ambos trabalharam no mesmo dia e na mesma obra (Obra C).
           
**Equação da Regressão Linear Simples:**  Y = aX + b
- Onde:               
    - **Y**: Variável dependente, produtividade do eletricista 
    - **X**: Variávek independente, produtividade do ajudante 
    - **a**: Coeficiente angular, que mostra quanto Y muda quando X aumenta em uma unidade.
    - **b**: Intercepto, o valor esperado de Y quando X é zero.

""")

st.write("Mas antes de começar as análises, iremos filtrar os dados pelos dias em que os ajudantes e os eletricistas trabalharam juntos na obra C. Foram filtrados 86 linhas. Abaixo colocamos as 10 primeiras linhas dos dados.")

# Carregando os dados diretamente do caminho local
excel_path = "dados/df_diarios.xlsx"
df = pd.read_excel(excel_path)

#Filtra apenas OBRA C
df_c = df[df['nome_obra']== 'OBRA_C']
df_instalacoes = df_c[df_c['grupo'] == 'INSTALACOES ELETRICAS']


df_filtrado_insumos = df_instalacoes[df_instalacoes['insumo'].isin(['AJUDANTE (SGSP)', 'ELETRICISTA (SGSP)'])].copy()

# Encontrar elementos que aparecem com ambos os insumos
elementos_comuns = df_filtrado_insumos.groupby('elemento')['insumo'].nunique()
elementos_para_manter = elementos_comuns[elementos_comuns == 2].index

# Filtrar o DataFrame original para manter apenas as linhas com os elementos comuns e os insumos desejados
df_regressao = df_filtrado_insumos[df_filtrado_insumos['elemento'].isin(elementos_para_manter)].copy()

st.dataframe(df_regressao.head(10))

st.markdown("""
- Analisar a força da correlação
- Equação resultante da regressão 
- Teste de hipótese para a regressão e/ou o coeficiente de deterninação (e no final deve decidir se a regressão é significativa ou não)
- Intervalo de confiança para o coeficiente angular e o intercepto
- Gráfico (Diagrama de dispersão entre X e Y) você pode colocar o IC da regressão.                   
""")

st.subheader("Correlação de Produtividade — AJUDANTE x ELETRICISTA (SGSP) — Instalações Elétricas")

# Garante que a coluna 'data' é datetime
df_regressao['data'] = pd.to_datetime(df_regressao['data'])

# Pivotar por elemento e data
df_pivotado = df_regressao.pivot_table(
    index=['elemento', 'data'],
    columns='insumo',
    values='ip_d'
).reset_index()

# Remove linhas onde falta algum dos insumos naquele elemento-dia
df_pivotado = df_pivotado.dropna(subset=['AJUDANTE (SGSP)', 'ELETRICISTA (SGSP)'])

st.write("Tabela comparativa de ip_d por elemento e data")
st.dataframe(df_pivotado.head(10))

# Calcula a correlação de Pearson
if not df_pivotado.empty:
    correlacao = df_pivotado['AJUDANTE (SGSP)'].corr(df_pivotado['ELETRICISTA (SGSP)'])
    st.markdown(f"##### Correlação de Pearson entre ip_d do AJUDANTE e do ELETRICISTA (mesmo elemento e data): **{correlacao:.2f}**")
else:
    st.warning("Não há dados suficientes para calcular a correlação após o filtro.")



st.write("Percebendo que existe uma alta correlação, seguiremos para a construção da equação da regressão linear. ")

st.subheader("Equação da Regressão Linear")

# Garante que não tem valores nulos nas duas colunas
df_plot = df_pivotado.dropna(subset=['AJUDANTE (SGSP)', 'ELETRICISTA (SGSP)'])

# Ajuste da regressão linear com statsmodels
X = df_plot['AJUDANTE (SGSP)']
Y = df_plot['ELETRICISTA (SGSP)']
X_const = sm.add_constant(X)  # Adiciona coluna de 1 para o intercepto
model = sm.OLS(Y, X_const).fit()
a = model.params[1]
b = model.params[0]
r2 = model.rsquared


# Exibe equação e R²
st.markdown(f"""
Equação ajustada:  
**ELETRICISTA (ip_d) = {a:.2f} × AJUDANTE (ip_d) + {b:.2f}**

Coeficiente de determinação (R²): **{r2:.2f}**
""")

st.subheader("Teste de hipótese")

# Teste de hipótese para o coeficiente angular (slope) e intercepto
p_val_angular = model.pvalues[1]   # p-valor para coeficiente angular
p_val_intercepto = model.pvalues[0]  # p-valor para o intercepto

st.markdown(f"#### Teste de hipótese para o coeficiente angular (slope)")
st.write(f"p-valor do coeficiente angular: **{p_val_angular:.4f}**")
if p_val_angular < 0.05:
    st.success("O coeficiente angular é estatisticamente significativo ao nível de 5%.")
else:
    st.warning("O coeficiente angular NÃO é estatisticamente significativo ao nível de 5%.")

st.markdown(f"#### Teste de hipótese para o intercepto")
st.write(f"p-valor do intercepto: **{p_val_intercepto:.4f}**")
if p_val_intercepto < 0.05:
    st.success("O intercepto é estatisticamente significativo ao nível de 5%.")
else:
    st.warning("O intercepto NÃO é estatisticamente significativo ao nível de 5%.")


st.subheader("Intervalo de confiança")

# Intervalos de confiança para os coeficientes (IC 95%)
conf_int = model.conf_int(alpha=0.05)  # 95% de confiança
ic_intercepto = conf_int.iloc[0].tolist()
ic_angular = conf_int.iloc[1].tolist()

st.markdown("#### Intervalo de confiança 95%")
st.write(f"IC do intercepto: **[{ic_intercepto[0]:.2f}, {ic_intercepto[1]:.2f}]**")
st.write(f"IC do coeficiente angular: **[{ic_angular[0]:.2f}, {ic_angular[1]:.2f}]**")


st.subheader("Gráfico e análise final")

# Valores para a reta e o IC
x_range = np.linspace(df_plot['AJUDANTE (SGSP)'].min(), df_plot['AJUDANTE (SGSP)'].max(), 100)
X_pred = sm.add_constant(x_range)
predictions = model.get_prediction(X_pred)
pred_summary = predictions.summary_frame(alpha=0.05)

# Gráfico interativo com Plotly
fig = go.Figure()

# Pontos observados
fig.add_trace(go.Scatter(
    x=df_plot['AJUDANTE (SGSP)'],
    y=df_plot['ELETRICISTA (SGSP)'],
    mode='markers',
    name='Observado',
    marker=dict(size=8, color='rgba(44, 160, 101, 0.8)'),
    text=[f"Elemento: {elem}<br>Data: {data.date()}" for elem, data in zip(df_plot['elemento'], df_plot['data'])],
    hoverinfo='text+x+y'
))

# Reta de regressão
fig.add_trace(go.Scatter(
    x=x_range,
    y=pred_summary['mean'],
    mode='lines',
    name='Regressão Linear',
    line=dict(color='firebrick', width=3)
))

# IC 95% (banda)
fig.add_trace(go.Scatter(
    x=np.concatenate([x_range, x_range[::-1]]),
    y=np.concatenate([pred_summary['mean_ci_upper'], pred_summary['mean_ci_lower'][::-1]]),
    fill='toself',
    fillcolor='rgba(255,0,0,0.15)',
    line=dict(color='rgba(255,255,255,0)'),
    hoverinfo="skip",
    name='IC 95% da Regressão'
))

fig.update_layout(
    title="Dispersão e Regressão Linear com Intervalo de Confiança",
    xaxis_title="Produtividade AJUDANTE (ip_d)",
    yaxis_title="Produtividade ELETRICISTA (ip_d)",
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
)

st.plotly_chart(fig, use_container_width=True)