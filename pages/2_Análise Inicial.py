import streamlit as st
import time
import pandas as pd
import numpy as np
import scipy.stats as stats
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotnine import *
from scipy.stats import norm

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

#titulo da página
st.header("Análise Inicial dos dados")

#Barra de carregamento
my_bar = st.progress(0)
for percent_complete in range(100):
     time.sleep(0.05)
     my_bar.progress(percent_complete + 1)


st.write("A tabela que temos que foi extraida de uma parte de um dataset que foi usada para renovar a tabela SIURB. Ambas as tabelas possuem milhares de informações sobre as mais diversas etapas das obra, desde a parte inicial da obra, como a remoção de terra, até mesmo etapas finais, com os revestimentos. Porém como o foco da nossa analise se trata das instalações elétricas, decidimos apresentar o dataframe abaixo com as informações já filtradas com os dados que vamos usar para a nossa análise.")

#leitura excel
excel_path = "dados/df_diarios.xlsx"
df = pd.read_excel(excel_path)
df1 = df.drop(['codigo_cc','nova'], axis = 1)

#filtrando pelos valores de cabos
valores_cabos = ['CABO 01', 'CABO 02', 'CABO 03', 'CABO 04']
df_cabos = df1[df1['classe'].isin(valores_cabos)]


#mostrando o dataset
st.dataframe(df_cabos)

st.subheader("Variáveis presentes no dataset")
st.markdown("""
- ***Classe:*** variável qualitativa nominal, que classifica as etapa da obra que está sendo medida pelos materiais e processos. Neste caso, está separado pelos tipos de cabos usados na obra.
- ***Caderno:*** variável qualitativa nominal, que classifica os tipos de obra, se são de infraestrutura, ou de edificios.
- ***Grupo:*** variável qualitativa nominal, que classifica o tipo da etapa da obra, se são revestimentos, ou instalação elétrica 
- ***Descrição:*** variável qualitativa nominal, que especifica o tipo de material empregado na obra.
- ***Unid:*** variável qualitativa nominal, que revela a unidade de medida que QS foi medida;
- ***Codins:*** variável quantitativa discreta, que representa o código insumo.
- ***Insumo:*** Variavél qualitativa nominal, que especifica o material ou mão de obra empregada na execução desta etapa da obra 
- ***Unidins:*** variável qualitativa nominal, que revela a unidade de medida que qntd foi medida;
- ***Tipo_insumo:*** variavel qualitativa nominal, que mostra o tipo de insumo utilizado
- ***Nome_obra:*** variável qualitativa continua, que informa o nome da obra; 
- ***Id_ccoi_elemento:*** variável quantitativa discreta, que mostra o id da classe de serviço.
- ***Id_appropriation_composition:*** variável quantitativa discreta, que informa o ID do que aconteceu ou não na obra;
- ***App_inicio:*** data e hora do inicio do serviço;
- ***App_fim:*** data e hora da conclusão do serviço;
- ***Qntd:*** variável quantitativa continua, que informa a horas utilizadas para executar o serviço naquele dia; 
- ***Qs:*** variável quantitativa continua, que mostra a quantidade de serviço realizado no dia;
- ***Data:*** informa a data do registro das informações;
- ***Qntd_acum:*** variável quantitativa continua, que informa a quantidade de horas acumuladas para executar o serviço;
- ***Qs_acum:*** variável quantitativa continua, que informa a quantidade de serviço acumulado;
- ***Ip_d:*** variável quantitativa contínua, que mostra o índice de produtividade diário;
- ***Ip_acum:*** variável quantitativa contínua, que informa o índice de prdutividade acumulado;
- ***Elemento:*** variável quantitativa discreta, que mostra qual a sequência de dados coletados. 
""")

st.subheader("Principais perguntas")
st.markdown("""
1. Qual a ⁠diferença de Produtividade entre eletricista e ajudante?
2. ⁠Qual o indice de produtividade/média de cada cabo?
3. ⁠Quais dias foram mais produtivos?
4. ⁠Qual a diferença do IP entre as obras C e D?
5. Qual a Diferença entre tipos de cabos e seus valores?
6. ⁠Existe um cabo mais utilizado, se sim porque?
""")
st.subheader("Principais Hipótese:")
st.markdown("""
- Acreditamos que haverá uma clara distinção de produtividade entre os cabos maiores e os cabos menores.
- Acreditamos que o Eletricista será mais produtivo que o ajudante.             
""")

st.subheader("Analisando a diferenças entre os cabos:")

st.write("Uma das principais coisas que percebemos ao verificar a base de dados é a existência de 04 tipos de cabos diferentes na coluna classe. Para melhor visualização e análise, decidimos filtrar as colunas por tipos de cabo.")

cabo_selecionado = st.selectbox("Selecione o tipo de cabo: ",valores_cabos)
df_filtrado = df_cabos[df_cabos['classe']== cabo_selecionado]
st.write(f"#### Dados para {cabo_selecionado}")
st.dataframe(df_filtrado)

st.write("Apesar dos cabos na tabela estarem separados em 04 categorias, ao analisarmos sua descrição, percebemos a existência de 06 tipos de cabos diferentes dos quais listamos abaixo quais são e seus preços por metro.")

dados_cabos = {
    "Código": ["Cabo 01", "Cabo 01", "Cabo 02", "Cabo 02", "Cabo 03", "Cabo 04"],
    "Descrição": [
        "Cabo flexível PVC - 750V - 3 condutores - 1,5mm²",
        "Cabo 1,00mm² - Isolamento para 0,7kV - Classe 4 - Flexível",
        "Cabo cobre flexível, isol. 750V não halogenado, antichama - 2,5mm²",
        "Cabo flexível PVC - 750V - 3 condutores - 2,50mm²",
        "Cabo cobre flexível, isol. 750V não halogenado, antichama - 4,0mm²",
        "Cabo 16,00mm² - Isolamento para 1,0kV - Classe 4 - Flexível"
    ],
    "Preço por metro (R$)": [1.24, 3.16, 2.58, 1.96, 3.26, 13.24]
}

df_cabos = pd.DataFrame(dados_cabos)

st.dataframe(df_cabos, use_container_width=True)

st.write("Ao realizar as pesquisas de preso, percebemos que o maior cabo, que é o CABO 04, é também o mais caro, custando mais de 13 reais o metro, enquanto os demais cabos variam entre 1 a 3 reais o metro.")

st.markdown("**Índice de Produtividade**")
st.write("O indice de produtividade, coluna IP_D, será a coluna que mais utilizaremos ao longo da nossa análise, pois como foi dito anteriormente, é o principal indicador de eficiência do setor. A fórmula utilizada para calcular o IP é:")
st.latex(r"IP = \frac{QNTD}{QS}")
st.markdown("""
Onde: 
- **QNTD** = Quantidade de tempo dedicada à atividade (em horas)
- **QS** = Quantidade de serviço realizada (em metros)
""")
st.write("Essa razão nos permite avaliar o tempo necessário por metro de cabo instalado, por exemplo.")