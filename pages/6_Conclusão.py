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

st.markdown("""
Este estudo permitiu uma análise detalhada da produtividade na construção civil, com foco nas instalações elétricas, reunindo evidências relevantes sobre a eficiência dos profissionais, o impacto dos materiais utilizados e a robustez dos processos de execução.

As comparações entre os tipos de cabos mostraram que, embora o Cabo 04 seja o mais caro, ele não se destacou em produtividade. Por outro lado, o Cabo 02B apresentou o melhor custo-benefício, combinando eficiência na execução com custo acessível — um dado valioso para a gestão de orçamentos em obras públicas e privadas.

Com relação ao desempenho das equipes, os testes de hipótese não identificaram diferença significativa entre a produtividade média de eletricistas e ajudantes. No entanto, a regressão linear revelou uma forte associação entre os dois grupos, com coeficiente de correlação de 0,95 e um R² de 0,90, o que indica que 90% da variação na produtividade dos eletricistas pode ser explicada pela produtividade dos ajudantes nos mesmos dias de trabalho. Essa interdependência revela que a atuação dos ajudantes tem papel direto no desempenho geral das equipes, e não pode ser considerada isoladamente.

O gráfico de regressão reforça visualmente essa conclusão. Os pontos observados concentram-se ao redor da linha de tendência, indicando baixa dispersão e alta previsibilidade. Além disso, o intervalo de confiança estreito demonstra a precisão do modelo ajustado, ampliando a segurança na interpretação dos resultados.

A análise integrada entre estatísticas descritivas, testes de hipótese e modelagem preditiva possibilitou uma compreensão aprofundada da dinâmica produtiva nas obras analisadas. Os resultados desafiam a percepção tradicional de que eletricistas atuam com produtividade superior de forma isolada, ao passo que destacam a importância da sinergia entre funções complementares no canteiro de obras. Em termos gerenciais, os achados reforçam a relevância de manter escalas bem coordenadas, utilizar os insumos de forma estratégica e basear as decisões em dados concretos. Concluímos, portanto, que a aplicação de métodos estatísticos à gestão da produtividade na construção civil é uma ferramenta poderosa para elevar a eficiência, reduzir desperdícios e qualificar a tomada de decisões — especialmente em projetos públicos que seguem parâmetros como os da Tabela SIURB.
""")
st.markdown(""" ----""")

st.subheader("Comentários de um Engenheiro Elétrico sobre o trabalho:")
st.write("O engenheiro expressa que não entendeu bem o trabalho, principalmente a tabela de cabos, onde não compreendeu a associação entre tipos de cabos, eletricistas e ajudantes. Ele sugere que todas as fórmulas usadas no trabalho sejam explicadas claramente, com definição dos termos (como o que é “IP”, “QNTD”, “QS”), acompanhadas de legendas e exemplos práticos. Ele também destaca que a produtividade não deve ser relacionada ao tipo de cabo, pois a escolha do cabo depende do dimensionamento da carga elétrica (ex: chuveiros exigem cabos de 4,0 mm ou 6,0 mm, não cabos menores). Segundo ele, um engenheiro eletricista não aceitaria essa lógica de associar produtividade ao cabo. Por fim, ele comenta que por se tratar de um trabalho de estatística, talvez a abordagem apresentada seja suficiente, desde que haja coerência e fundamentação nas fórmulas.")