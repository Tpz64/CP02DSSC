import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
import plotly.graph_objects as go
import time

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


#leitura excel
excel_path = "dados/df_diarios.xlsx"
df = pd.read_excel(excel_path)
df1 = df.drop(['codigo_cc','nova'], axis = 1)

#filtrando pelos valores de cabos
valores_cabos = ['CABO 01', 'CABO 02', 'CABO 03', 'CABO 04']
df_cabos = df1[df1['classe'].isin(valores_cabos)]


st.header("Intervalo de confiança")

#Barra de carregamento
my_bar = st.progress(0)
for percent_complete in range(100):
     time.sleep(0.05)
     my_bar.progress(percent_complete + 1)

st.write("O intervalo de confiança é uma ferramenta estatística utilizada para estimar, com determinado nível de certeza, um valor populacional com base em uma amostra. Em vez de fornecer apenas uma média, o intervalo de confiança indica uma faixa na qual, com uma certa probabilidade (como 95%), acredita-se que o valor verdadeiro se encontra. Isso é especialmente útil quando se trabalha com dados amostrais e há incertezas envolvidas.")
st.write("Na prática, usamos o intervalo de confiança para entender a variabilidade dos dados e a confiabilidade das estimativas. Quanto menor o intervalo, mais precisa é a estimativa; quanto maior, mais incerteza ela carrega.")
st.write("Analisamos os indicadores de produtividade (coluna ip_d) para os cabos identificados como CABO 01 a CABO 04. Para cada tipo de cabo, foi calculado um intervalo de confiança de 95%, com base nos dados registrados no sistema.")

st.subheader("Intervalo de Confiança por Tipo de Cabo")

# Cálculo do intervalo de confiança para cada tipo de cabo
confidence_data = {
    "Cabo": [],
    "Média": [],
    "Inferior": [],
    "Superior": []
}

for cabo in valores_cabos:
    data = df_cabos[df_cabos['classe'] == cabo]['ip_d']
    if len(data) > 1:  # Garante que haja dados suficientes
        mean = np.mean(data)
        sem = stats.sem(data)  # Standard error of the mean
        interval = stats.t.interval(0.95, len(data)-1, loc=mean, scale=sem)
        confidence_data["Cabo"].append(cabo)
        confidence_data["Média"].append(mean)
        confidence_data["Inferior"].append(interval[0])
        confidence_data["Superior"].append(interval[1])

# Transformando em DataFrame para usar com Plotly
df_conf = pd.DataFrame(confidence_data)

# Cálculo do erro para barras (yerr)
df_conf["Erro Inferior"] = df_conf["Média"] - df_conf["Inferior"]
df_conf["Erro Superior"] = df_conf["Superior"] - df_conf["Média"]

#Grafico
# Selecionando e renomeando colunas para exibição
tabela = df_conf[["Cabo", "Média", "Inferior", "Superior"]].copy()
tabela.columns = ["Cabo", "Média", "Limite Inferior", "Limite Superior"]

# Exibindo a tabela no Streamlit
st.dataframe(tabela, use_container_width=True)

# Gráfico interativo com Plotly
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df_conf["Cabo"],
    y=df_conf["Média"],
    mode='markers',
    name='Média ip_d',
    error_y=dict(
        type='data',
        symmetric=False,
        array=df_conf["Erro Superior"],
        arrayminus=df_conf["Erro Inferior"],
        color='gray',
        thickness=1.5,
        width=6
    ),
    marker=dict(size=10, color='gold')
))

fig.update_layout(
    title="Intervalo de Confiança da ip_d por Tipo de Cabo",
    xaxis_title="Tipo de Cabo",
    yaxis_title="Média de ip_d",
    height=500
)

st.plotly_chart(fig, use_container_width=True)

st.write("Embora estatisticamente os intervalos de confiança se sobreponham, sugerindo que não há diferença significativa entre os tipos de cabo, na prática essa diferença pode impactar o planejamento de mão de obra. Para isso, faremos uma análise mais profuda da instalação e custos. ")
st.write("Assim, o intervalo de confiança não apenas reforça a robustez dos dados, como também auxilia na tomada de decisão prática, mesmo quando a diferença estatística não é clara.")

st.subheader("Análise de Instalação e custos")

st.write("Imaginando a obra de um prédio de 8 andares, onde cada andar possua 10 salas, e que em cada sala, seriam utilizados 50 metros de cabos, totalizamos que 4000 metros de cabos seriam instalados nesse edifício.")
st.write("Supondo que a equipe de instalação dessa obra seja composta por 3 pessoas, onde a carga horária por dia seria de 8 horas por pessoa, isso totalizaria 24 horas de tempo disponível por dia da equipe.")

# Dados de tempo por cabo
tempo_dados = {
    "Cabo": ["Cabo 1", "Cabo 2", "Cabo 3", "Cabo 4"],
    "Inferior (h)": [201.9, 142.9, 155.3, 66.0],
    "Média (h)": [388.8, 206.5, 155.3, 173.7],
    "Superior (h)": [575.7, 269.9, 441.3, 281.4],
    "Dias úteis (média)": [16.2, 8.6, 6.5, 7.2]
}

df_tempo = pd.DataFrame(tempo_dados)
st.markdown("<h5>Estimativa de Tempo de Instalação (Equipe de 3 pessoas, 8h/dia)</h5>", unsafe_allow_html=True)
st.dataframe(df_tempo, use_container_width=True)

# Dados de custo dos cabos
st.markdown("<h4>Custo de Material por Cabo</h4>", unsafe_allow_html=True)

cabo_1_data = {
    "Modelo": ["A", "B"],
    "Descrição": [
        "Cabo flexível PVC - 750V - 3 condutores - 1,5mm²",
        "Cabo 1,00mm² - Isolamento p/ 0,7kV - Classe 4 - Flexível"
    ],
    "Preço (R$/m)": [1.24, 3.16],
    "Custo Total (R$)": [1.24 * 4000, 3.16 * 4000]
}
df_cabo1 = pd.DataFrame(cabo_1_data)
st.markdown("**Cabo 01**")
st.dataframe(df_cabo1, use_container_width=True)

cabo_2_data = {
    "Modelo": ["A", "B"],
    "Descrição": [
        "Cabo cobre flexível, isol. 750V não halogenado, antichama - 2,5mm²",
        "Cabo flexível PVC - 750V - 3 condutores - 2,50mm²"
    ],
    "Preço (R$/m)": [2.58, 1.96],
    "Custo Total (R$)": [2.58 * 4000, 1.96 * 4000]
}
df_cabo2 = pd.DataFrame(cabo_2_data)
st.markdown("**Cabo 02**")
st.dataframe(df_cabo2, use_container_width=True)

cabo_3_data = {
    "Descrição": [
        "Cabo cobre flexível, isol. 750V não halogenado, antichama - 4,0mm²"
    ],
    "Preço (R$/m)": [3.26],
    "Custo Total (R$)": [3.26 * 4000]
}
df_cabo3 = pd.DataFrame(cabo_3_data)
st.markdown("**Cabo 03**")
st.dataframe(df_cabo3, use_container_width=True)

cabo_4_data = {
    "Descrição": [
        "Cabo 16,00mm² - Isolamento p/ 1,0kV - Classe 4 - Flexível"
    ],
    "Preço (R$/m)": [13.24],
    "Custo Total (R$)": [13.24 * 4000]
}
df_cabo4 = pd.DataFrame(cabo_4_data)
st.markdown("**Cabo 04**")
st.dataframe(df_cabo4, use_container_width=True)

# Comparativo
comparativo_data = {
    "Cabo": [
        "Cabo 1 (A)", "Cabo 1 (B)",
        "Cabo 2 (A)", "Cabo 2 (B)",
        "Cabo 3", "Cabo 4"
    ],
    "Custo Total Material (R$)": [
        4960.00, 12640.00,
        10320.00, 7840.00,
        13040.00, 52960.00
    ],
    "Tempo Médio (h)": [
        388.8, 388.8,
        206.5, 206.5,
        155.3, 173.7
    ],
    "Dias úteis (Equipe)": [
        16.2, 16.2,
        8.6, 8.6,
        6.5, 7.2
    ]
}
df_comparativo = pd.DataFrame(comparativo_data)
st.markdown("<h4>Comparativo Geral (Custo x Tempo Médio)</h4>", unsafe_allow_html=True)
st.dataframe(df_comparativo, use_container_width=True)

st.write("Com base na última tabela, concluímos que o Cabo 02B apresenta o melhor custo-benefício, equilibrando adequadamente tempo de instalação e valor. Embora o Cabo 01A seja o mais barato, ele demanda um tempo maior para instalação. Já o Cabo 03 se destaca pela agilidade na execução, porém com um custo mais elevado. Por fim, o Cabo 04 é o menos vantajoso, pois representa o maior custo tanto em termos de tempo quanto de investimento financeiro.")


st.markdown("""
            ----------
**Parte 1**
            
Iremos fazer em aula, no dia 04 de abril.
            
Entregar até o dia 11/04 antes da aula.
            
• Deverá conter:
- Aplicação e visualização de Intervalos de Confiança
- Interpretação prática com base no contexto do dataset 
- Visualizações e interpretação dos resultados
""")