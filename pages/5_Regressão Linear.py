import streamlit as st
import pandas as pd
import time 
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
No contexto desta análise, queremos saber se a produtividade do ajudante está relacionada à do eletricista, considerando apenas os casos em que ambos trabalharam no mesmo dia e na mesma obra, que neste caso é a C.
           
**Equação da Regressão Linear Simples:  y = ax + b **
- Onde:               
    - **y**: Variável dependente (produtividade do eletricista) 
    - **x**: Variável independente (produtividade do ajudante) 
    - **a**: Coeficiente angular (indica quanto Y muda quando X aumenta em uma unidade)
    - **b**: Intercepto (valor esperado de Y quando X é zero)

""")

st.write("Antes de iniciarmos, filtramos os dados para considerar somente os dias em que eletricistas e ajudantes trabalharam juntos na Obra C. Abaixo, mostramos as 10 primeiras linhas dos dados filtrados.")

# Carregando os dados diretamente do caminho local
excel_path = "dados/df_diarios.xlsx"
df = pd.read_excel(excel_path)

# Filtra apenas OBRA C e INSTALAÇÕES ELÉTRICAS
df_c = df[df['nome_obra'] == 'OBRA_C']
df_instalacoes = df_c[df_c['grupo'] == 'INSTALACOES ELETRICAS']

# Filtra apenas os insumos de interesse
df_filtrado_insumos = df_instalacoes[df_instalacoes['insumo'].isin(['AJUDANTE (SGSP)', 'ELETRICISTA (SGSP)'])].copy()

# Converte a coluna 'data' para datetime (caso não esteja) e extrai apenas a data
df_filtrado_insumos['data'] = pd.to_datetime(df_filtrado_insumos['data']).dt.date

# Mantém apenas as datas onde existam ambos os insumos
datas_comuns = df_filtrado_insumos.groupby('data')['insumo'].nunique()
datas_validas = datas_comuns[datas_comuns == 2].index

# Filtra o DataFrame pelas datas válidas
df_regressao = df_filtrado_insumos[df_filtrado_insumos['data'].isin(datas_validas)].copy()

# Visualização de amostra
st.dataframe(df_regressao.head(10))

##CORRELACAO
st.subheader("Correlação de Produtividade — AJUDANTE x ELETRICISTA")

st.write("O primeiro passo da análise foi calcular a **correlação entre as produtividades** do ajudante e do eletricista nas instalações elétricas realizadas no mesmo dia. Se a correlação for alta, justifica-se aplicar a regressão linear.")

# Garante que a coluna 'data' é datetime
df_regressao['data'] = pd.to_datetime(df_regressao['data']).dt.date

# Pivotar por elemento e data
df_pivotado = df_regressao.pivot_table(
    index=['data'],
    columns='insumo',
    values='ip_d'
).reset_index()

# Remove linhas onde falta algum dos insumos naquele elemento-dia
df_pivotado = df_pivotado.dropna(subset=['AJUDANTE (SGSP)', 'ELETRICISTA (SGSP)'])

st.dataframe(df_pivotado)

st.write("Aplicamos o coeficiente de correlação de Pearson, que mede a intensidade da associação linear entre duas variáveis.")

with st.expander("Explicação da Correlação de Pearson"):
    st.markdown(r"""
    A correlação de Pearson mede a intensidade e a direção da relação linear entre duas variáveis numéricas.

    O coeficiente de correlação de Pearson varia entre -1 e 1:
    
    - **+1**: Correlação linear positiva perfeita  
    - **0**: Ausência de correlação linear  
    - **-1**: Correlação linear negativa perfeita  

    Características principais:
    - Presume que as variáveis seguem uma distribuição normal
    - Sensível a outliers
    - Indica **associação**, mas não implica **causalidade**

    É amplamente utilizado para avaliar o grau de linearidade entre dois conjuntos de dados.
    """)

st.write("Veja o resultado abaixo:")

# Calcula a correlação de Pearson
if not df_pivotado.empty:
    correlacao = df_pivotado['AJUDANTE (SGSP)'].corr(df_pivotado['ELETRICISTA (SGSP)'])
    st.info(f"Correlação de Pearson entre ip_d do AJUDANTE e do ELETRICISTA: **{correlacao:.2f}**")

else:
    st.warning("Não há dados suficientes para calcular a correlação após o filtro.")

st.write("O resultado próximo de 1, revela uma **correlação positiva forte**, indicando que há uma associação linear significativa entre as variáveis. Com isso, seguimos para a construção da equação da regressão linear.")

st.subheader("Equação da Regressão Linear")

st.write("""
Como vimos anteriormente, a equação da regressão linear é composta por dois parâmetros principais: o **coeficiente angular (inclinação)** e o **intercepto**.  
Para calcular esses valores, utilizamos bibliotecas especializadas do Python, como a `statsmodels`, que oferece ferramentas estatísticas robustas para ajustar modelos, interpretar resultados e conduzir análises de regressão de forma precisa e confiável.
""")
st.write("""
Além de estimar os coeficientes da regressão, o modelo também calcula o **coeficiente de determinação (R²)** — um indicador essencial da qualidade do ajuste.

O R² mostra a proporção da variação da variável dependente que é explicada pela variável independente.  
- Quanto mais próximo de **1**, melhor o modelo representa os dados.
- Quanto mais próximo de **0**, menor o poder explicativo da equação.

Em outras palavras, o R² nos ajuda a entender **o quão bem a linha de regressão se ajusta aos dados observados**.
""")

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
st.markdown("""
Abaixo está a equação da regressão linear, com os coeficientes já calculados, além do **R²**, que indica a qualidade do modelo:
""")

st.code(f"ELETRICISTA (ip_d) = {a:.2f} × AJUDANTE (ip_d) + {b:.3f}", language="python")

st.markdown(f"""
 **Coeficiente de determinação (R²) = {r2:.2f}** 
""")

st.write("O coeficiente de determinação perto de 1 indica o quanto da variação na produtividade do eletricista é explicada pela produtividade do ajudante.")

##TESTE DE HIPOTESE
st.subheader("Teste de hipótese dos coeficientes")

# Teste de hipótese para o coeficiente angular (slope) e intercepto
p_val_angular = model.pvalues[1]   # p-valor para coeficiente angular
p_val_intercepto = model.pvalues[0]  # p-valor para o intercepto

st.write("""
Nesta etapa, avaliamos se os coeficientes da regressão — o **coeficiente angular (a)** e o **intercepto (b)** — são realmente relevantes para explicar a relação entre as variáveis.

Para isso, usamos o **teste t de Student**, que calcula o **p-valor**: uma medida que indica a chance de o resultado ter ocorrido por acaso.

As hipóteses testadas são:
- **Hipótese nula (H₀):** o coeficiente é igual a zero (não tem efeito significativo no modelo).
- **Hipótese alternativa (H₁):** o coeficiente é diferente de zero (tem efeito significativo).

- Se o **p-valor for menor que 0,05 (5%)**, rejeitamos a hipótese nula e consideramos o coeficiente **estatisticamente significativo**, ou seja, com efeito real.
- Se for maior que 0,05, o resultado pode ter sido apenas uma flutuação dos dados.

Esse teste nos ajuda a saber se vale a pena confiar nos coeficientes calculados pela regressão.
""")

# Teste para o coeficiente angular
st.markdown("##### Coeficiente Angular (a)")
st.write(f"**p-valor:** {p_val_angular:.4f}")
if p_val_angular < 0.05:
    st.success("Resultado: O coeficiente angular é estatisticamente significativo (p < 0.05). Isso indica que a variável independente (produtividade do ajudante) tem efeito relevante na variável dependente (produtividade do eletricista).")
else:
    st.warning("Resultado: O coeficiente angular **não** é estatisticamente significativo (p ≥ 0.05), o que sugere que a variável independente pode não ter impacto relevante sobre a variável dependente neste modelo.")

# Teste para o intercepto
st.markdown("##### Intercepto (b)")
st.write(f"**p-valor:** {p_val_intercepto:.4f}")
if p_val_intercepto < 0.05:
    st.success("Resultado: O intercepto é estatisticamente significativo. Isso indica que, mesmo com produtividade do ajudante igual a zero, há uma produtividade média prevista para o eletricista.")
else:
    st.warning("Resultado: O intercepto não é estatisticamente significativo. Isso pode indicar que o valor base do eletricista (quando o ajudante tem produtividade zero) não difere estatisticamente de zero.")

# Decisão final
st.markdown("##### Conclusão sobre a Regressão")
if p_val_angular < 0.05:
    st.success("Com base no teste de hipótese, a regressão é estatisticamente significativa. O modelo é válido para explicar a relação entre as variáveis.")
else:
    st.error("A regressão não é estatisticamente significativa. Recomenda-se revisar o modelo ou verificar outros fatores que possam influenciar a variável dependente.")


##INTERVALO DE CONFIANCA
st.subheader("Intervalo de confiança dos coeficientes")

st.write("""
Para reforçar a análise, calculamos o **intervalo de confiança (IC)** de 95% para os coeficientes da regressão. A estimativa e o IC foram obtidos utilizando a biblioteca `statsmodels`, que oferece ferramentas estatísticas avançadas para modelos lineares.
""")

# Intervalos de confiança para os coeficientes
conf_int = model.conf_int(alpha=0.05)
ic_intercepto = conf_int.iloc[0].tolist()
ic_angular = conf_int.iloc[1].tolist()

st.markdown(f"""
- **Intercepto (b):**  \\[ {ic_intercepto[0]:.3f},\ {ic_intercepto[1]:.3f} \\]

- **Coeficiente angular (a):**  \\[ {ic_angular[0]:.2f},\ {ic_angular[1]:.2f} \\]
""")

st.write("Os resultados indicam intervalos relativamente estreitos, especialmente para o coeficiente angular, o que sugere uma baixa variabilidade nas estimativas. Isso reforça a confiabilidade estatística do modelo, demonstrando que a produtividade do ajudante é um bom preditor da produtividade do eletricista dentro da amostra analisada.")

##GRAFICO FINAL
st.subheader("Gráfico")

st.write("O gráfico abaixo mostra visualmente a relação entre as variáveis:")

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
    text=[f"Data: {data}" for data in df_plot['data']],
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

st.write("""
**Elementos**:
- **Pontos verdes:** Observações reais dos dados (produtividade empírica).
- **Linha vermelha:** Equação da regressão linear ajustada.
- **Faixa rosa clara:** Intervalo de confiança de 95% para a regressão.
""")

st.write(""" A linha de tendência mostra uma **relação linear positiva** clara entre as variáveis: quando a produtividade do ajudante aumenta, a produtividade do eletricista também tende a aumentar. Já a **concentração dos pontos ao redor da linha** sugere uma boa aderência do modelo aos dados. O **intervalo de confiança estreito** indica que há pouca incerteza nas estimativas feitas pela regressão. E apesar de alguns pontos mais afastados (potenciais outliers), eles ainda se encontram dentro do intervalo de confiança, o que mostra que o modelo é robusto frente a pequenas variações.""")
st.write("A conclusão é que o  gráfico confirma visualmente que há uma **forte associação linear positiva** entre as variáveis analisadas. A regressão apresenta **alta confiabilidade**, baixa dispersão e é uma ferramenta válida para prever a produtividade do eletricista com base na do ajudante.")