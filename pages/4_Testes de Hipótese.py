import streamlit as st

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

st.header("Testes de hipóteses")
st.subheader("Parte 2")
st.write("Iremos fazer em aula, no dia 11 de abril.")
st.write("Entregar até o dia 25/04 antes da aula.")
st.markdown("""
• Deverá conter:
- Formulação de hipóteses nula e alternativa
- Aplicação de pelo menos dois testes estatísticos (t, z, proporção, qui-quadrado, outros)
- Visualizações e interpretação dos resultados
""")