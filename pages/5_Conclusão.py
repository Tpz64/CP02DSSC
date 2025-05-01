import streamlit as st
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

st.header("Conclusão")

#Barra de carregamento
my_bar = st.progress(0)
for percent_complete in range(100):
     time.sleep(0.05)
     my_bar.progress(percent_complete + 1)

st.write("Em conclusão, a análise da produtividade na construção civil, especialmente no setor elétrico, revelou insights importantes sobre o desempenho das equipes, custos e escolha dos materiais. O índice de produtividade (IP_d) mostrou-se essencial para avaliar a eficiência das obras e otimizar os processos construtivos, proporcionando informações cruciais para o planejamento e controle de custos. Ao examinar os diferentes tipos de cabos utilizados nas obras, observou-se que, embora o Cabo 04 seja o mais caro, ele não se destacou em termos de produtividade, sendo o Cabo 02B o mais vantajoso em termos de custo-benefício.")
st.write("A análise estatística, por meio de testes de hipótese, indicou que não há uma diferença significativa na produtividade entre eletricistas e ajudantes. Ambos os grupos apresentaram resultados semelhantes, o que sugere que, sob as condições específicas da análise, não há uma vantagem clara para o eletricista em termos de produtividade.")
st.write("Esse estudo destaca a importância da análise detalhada dos dados para a otimização dos processos na construção civil, permitindo decisões mais informadas sobre os materiais e a alocação de mão de obra. Embora os resultados não tenham mostrado grandes disparidades entre as categorias de trabalhadores, a contínua análise de dados e ajustes nos processos são fundamentais para o aumento da produtividade e a redução de custos nas obras.")

st.markdown(""" ----""")

st.subheader("Comentários de um Engenheiro Elétrico sobre o trabalho:")
st.write("O engenheiro expressa que não entendeu bem o trabalho, principalmente a tabela de cabos, onde não compreendeu a associação entre tipos de cabos, eletricistas e ajudantes. Ele sugere que todas as fórmulas usadas no trabalho sejam explicadas claramente, com definição dos termos (como o que é “IP”, “QNTD”, “QS”), acompanhadas de legendas e exemplos práticos. Ele também destaca que a produtividade não deve ser relacionada ao tipo de cabo, pois a escolha do cabo depende do dimensionamento da carga elétrica (ex: chuveiros exigem cabos de 4,0 mm ou 6,0 mm, não cabos menores). Segundo ele, um engenheiro eletricista não aceitaria essa lógica de associar produtividade ao cabo. Por fim, ele comenta que por se tratar de um trabalho de estatística, talvez a abordagem apresentada seja suficiente, desde que haja coerência e fundamentação nas fórmulas.")