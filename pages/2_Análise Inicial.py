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
        background-color: #ffff; 
        color:white;
        padding: 9px; 
        border-radius: 10px;
        text-align: center;
    ">
        <p style="color:black; font-weight: bold;">Desenvolvido por:</p>
        <div>
            <a href="https://www.linkedin.com" target="_blank" 
               style="color: black; text-decoration: none; font-weight: bold;">
                André de Sousa Neves
            </a>
        </div>
        <div>
            <a href="https://www.linkedin.com" target="_blank" 
               style="color: black; text-decoration: none; font-weight: bold;">
                Beatriz Dantas Sampaio
            </a>
        </div>
        <div>
            <a href="https://www.linkedin.com" target="_blank" 
               style="color: black; text-decoration: none; font-weight: bold;">
                Isabela Barcellos Freire
            </a>
        </div>
        <div>
            <a href="https://www.linkedin.com/in/thaisgleoncio/" target="_blank" 
               style="color: black; text-decoration: none; font-weight: bold;">
                Thaís Leoncio
            </a>
        </div>
    </div>
""", unsafe_allow_html=True)

#titulo da página
st.header("Analise Inicial dos dados")

#Barra de carregamento
my_bar = st.progress(0)
for percent_complete in range(100):
     time.sleep(0.05)
     my_bar.progress(percent_complete + 1)


st.write("A tabela original possui milhares de informações sobre as mais diversas etapas das obra, desde a parte inical, como a remoção de material, até mesmo etapas finais, com os revestimentos. Porém como o foco da nossa analise se trata das instalações eletricas, decidimos apresentar o dataframe abaixo com as informações já filtradas.")

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
""")

st.subheader("Diferenças entre os cabos:")

cabo_selecionado = st.selectbox("Selecione o tipo de cabo: ",valores_cabos)
df_filtrado = df_cabos[df_cabos['classe']== cabo_selecionado]
st.write(f"#### Dados para {cabo_selecionado}")
st.dataframe(df_filtrado)

st.write("Os cabos na tabela estão separados em 04 categorias, porém ao analisarmos sua descrição, percebemos a existência de 06 tipos de cabos diferentes dos quais listamos abaixo quais são e seus preços por metro.")
st.markdown("""
1. CABO 01 -> CABO FLEXÍVEL PVC-750V - 3 CONDUTORES - 1,5MM2 -> R$ 1,24/mt
2. CABO 01 -> CABO 1,00MM2 - ISOLAMENTO PARA 0,7KV - CLASSE 4 - FLEXÍVEL -> R$ 3,16/mt            
3. CABO 02 -> CABO COBRE FLEXÍVEL, ISOL. 750V NÃO HALOGENADO, ATICHAMA - 2,5MM2 -> R$ 2,58/mt
4. CABO 02 -> CABO FLEXÍVEL PVC - 750V - 3 CONDUTORES - 2,50MM2 -> R$ 1,96/mt
5. CABO 03 -> CABO COBRE FLEXÍVEL, ISOL. 750V NÃO HALOGENADO, ANTICHAMA - 4,0MM2 -> R$ 3,26/mt
6. CABO 04 -> CABO 16,00MM2 - ISOLAMENTO PARA 1,0KV - CLASSE 4 - FLEXÍVEL -> R$ 13,24/mt 
""")

st.write("Percebemos que o maior cabo, que é o CABO 04, é também o mais caro, custando mais de 13 reais o metro, enquanto que os outro variam entre 1 a 3 reais o metro.")

st.markdown("""
            ---------
Parte 0 – Introdução ao Problema e à Base de Dados (obrigatório)
- Apresentação clara do problema ou contexto de mercado
- Descrição da base de dados e variáveis
- Identificação de perguntas de análise e possíveis hipóteses
- Conexão entre o problema real e o que será desenvolvido no
dashboard
- Organização inicial do layout e estrutura do dashboard
""")