import streamlit as st 

st.set_page_config(page_title="Produtividade construção", layout="wide")

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

#Inicio análise
#st.markdown("")
st.header("Introdução do caso")
st.write("Colocar texto inicial aqui. Descrição do problema ou contexto do mercado")
st.write("A análise que será abordada neste estudo enfoca obras elétricas, com o objetivo de avaliar a qualidade de cada projeto, o tempo de execução e os materiais empregados. Esse processo busca aprimorar as previsões para futuras obras, otimizar a qualidade dos serviços prestados e compreender melhor o fluxo de desenvolvimento dessas obras.")

st.markdown("""
Parte 0 – Introdução ao Problema e à Base de Dados (obrigatório)
- Apresentação clara do problema ou contexto de mercado
- Descrição da base de dados e variáveis
- Identificação de perguntas de análise e possíveis hipóteses
- Conexão entre o problema real e o que será desenvolvido no
dashboard
- Organização inicial do layout e estrutura do dashboard
""")
