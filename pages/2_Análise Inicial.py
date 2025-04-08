import streamlit as st
import time

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

st.write("Os dados que temos vieram daqui.")
st.write("Os dados que usaremos para essa análise são esses")
st.write("Colocar aqui as variaveis comentadas")

st.write("Perguntas de analise e possíveis hipoteses")

st.write("Conexão entre o problema real e o que será desenvolvido no dashboard -> lembrando que a base de dados que temos é apenas uma amostra. ")



st.write("textinho inicial aqui. Apresentação do dataset e suas variáveis")

st.write("Apresentação do dataset e suas variáveis")

st.write("Identificação de possíveis hipóteses e perguntas investigativas")

st.write("Preparação do ambiente inicial do dashboard (layout e estrutura)")

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