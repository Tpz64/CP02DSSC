import streamlit as st 

st.set_page_config(page_title="Produtividade construção", layout="wide")

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
            <a href="https://www.linkedin.com" target="_blank" 
               style="color: black; text-decoration: none;">
                André de Sousa Neves
            </a>
        </div>
        <div>
            <a href="https://www.linkedin.com" target="_blank" 
               style="color: black; text-decoration: none;">
                Beatriz Dantas Sampaio
            </a>
        </div>
        <div>
            <a href="https://www.linkedin.com" target="_blank" 
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

#Inicio análise
#st.markdown("")
st.header("Introdução do caso")
st.write("A construção civil é um dos setores mais importantes para o desenvolvimento socioeconômico de um país, sendo responsável por obras de infraestrutura, habitação e urbanização. Seu impacto direto na geração de empregos, movimentação da economia e melhoria da qualidade de vida torna essencial o aprimoramento constante de suas práticas. Nesse contexto, a produtividade na construção civil se destaca como um dos principais indicadores de eficiência do setor.")
st.write("O índice de produtividade na construção civil é utilizado para medir o desempenho das equipes ou dos processos executivos de uma obra, demonstrando quanto de determinado serviço é produzido em um intervalo de tempo com os recursos disponíveis. Sua fórmula básica é:")
st.latex(r"Produtividade = \frac{Quantidade Produzida}{Recursos Utilizados}")
st.write("Esse índice permite aos gestores planejar com maior precisão, controlar custos, otimizar o uso de materiais e mão de obra, além de identificar gargalos nos processos construtivos. Com ele, é possível promover a melhoria contínua dos métodos de execução, resultando em obras mais rápidas, econômicas e sustentáveis.")
st.write("Neste dashboard iremos analisar uma base de dados já tratada que foi utilizada para a atualização da tabela SIURB, uma tabela que é desenvolvida pela Secretaria Municipal de Infraestrutura Urbana e Obras, que reúne composições de custos unitários de serviços, preços de insumos e índices de produtividade da mão de obra, sendo utilizada como referência obrigatória em orçamentos de obras públicas municipais.")

#Aqui colocar em colunas/ de um lado 
col1, col2 = st.columns([2,2])

with col1:
    st.write("A análise que será abordada neste estudo tem como foco obras elétricas, com o objetivo de avaliar a qualidade de cada projeto, o tempo de execução e os materiais empregados. Esse processo busca aprimorar as previsões para futuras obras, otimizar a qualidade dos serviços prestados e compreender melhor o fluxo de desenvolvimento dessas obras.")
    st.write("Por se tratar de uma amostra, as análises contidas neste dashbord podem estar sujeitas a alterações.")

with col2: 
    st.image("imgs/img-instalacao-eletrica.jpg",width=400)
