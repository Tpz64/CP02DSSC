import streamlit as st
import pandas as pd
from scipy.stats import ttest_ind, mannwhitneyu
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


st.header("Testes de hipóteses")

#Barra de carregamento
my_bar = st.progress(0)
for percent_complete in range(100):
     time.sleep(0.05)
     my_bar.progress(percent_complete + 1)

st.markdown("""
O teste de hipótese é uma técnica estatística que nos ajuda a tomar decisões sobre populações com base nos dados observados de uma amostra. Ele nos permite avaliar se há evidências suficientes para apoiar ou rejeitar uma **hipótese estatística previamente formulada**.

Durante esse processo, definimos:

- A **hipótese nula (H₀)** — geralmente representa a ausência de efeito ou diferença.
- A **hipótese alternativa (H₁)** — representa a presença de um efeito ou diferença.
- Um **nível de significância** (geralmente 5%) — que define o limite de probabilidade para rejeitar H₀.

Com isso, escolhemos o teste mais adequado (paramétrico ou não paramétrico), calculamos a **estatística do teste** e obtemos o **valor-p**.

A **decisão** segue a lógica:

- Se o **valor-p for menor ou igual ao nível de significância**, rejeitamos H₀.
- Caso contrário, **não rejeitamos H₀**, ou seja, não encontramos evidência estatística suficiente para descartá-la.

Com base na nossa análise de produtividade, formulamos a hipótese que será testada a seguir.
""", unsafe_allow_html=True)
st.subheader("Produtividade Eletricista vs Ajudante")

st.markdown("""
Antes de analisarmos os dados em profundidade, levantamos a hipótese de que o **eletricista é mais produtivo que o ajudante**. Para realizar o teste estatístico adequado, definimos a **hipótese nula**, a **hipótese alternativa** e o **nível de significância**, conforme descrito abaixo:


- **Hipótese nula (H₀):** A produtividade do eletricista é menor ou igual à do ajudante (não há diferença significativa).
- **Hipótese alternativa (H₁):** A produtividade do eletricista é maior que a do ajudante.
- **Nível de significância:** Utilizaremos o valor padrão de **0,05 (5%)**.        
""")

# Carregando os dados diretamente do caminho local
excel_path = "dados/df_diarios.xlsx"
df = pd.read_excel(excel_path)

# Lista dos tipos de cabos que você quer considerar (ajuste conforme seus dados)
cabos_validos = [
    "CABO 01",
    "CABO 02",
    "CABO 03",
    "CABO 04"
]

# Filtro por grupo e por classe (cabos)
df_instalacoes = df[
    (df['grupo'].str.upper() == 'INSTALACOES ELETRICAS') &
    (df['classe'].str.upper().isin(cabos_validos))
]

# Filtra apenas os insumos específicos
df_eletricista = df_instalacoes[df_instalacoes['insumo'].str.upper() == 'ELETRICISTA (SGSP)']
df_ajudante = df_instalacoes[df_instalacoes['insumo'].str.upper() == 'AJUDANTE (SGSP)']

# Verifica se há dados
if not df_eletricista.empty and not df_ajudante.empty:
    eletricista_ip = df_eletricista["ip_d"].dropna()
    ajudante_ip = df_ajudante["ip_d"].dropna()

    st.markdown("""<h4>Resumo Estatístico</h4>""", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Eletricistas (SGSP)**")
        st.dataframe(eletricista_ip.describe().to_frame())
    with col2:
        st.markdown("**Ajudantes (SGSP)**")
        st.dataframe(ajudante_ip.describe().to_frame())
    
    st.write("Ao analisar o resumo estatístico, percebemos que a quantidade de eletricistas na instalação das obras é maior do que a de ajudantes.")
    st.write(
        "Nesta análise, utilizamos dois testes:\n\n"
        "- **Teste t de Student**: compara as médias das produtividades.\n"
        "- **Teste U de Mann-Whitney**: alternativa não paramétrica ao teste t, usada quando os dados não seguem uma distribuição normal."
    )

    st.markdown("""<h4>Resultado do Teste t de Student</h4>""", unsafe_allow_html=True)

    with st.expander("Explicação do Teste t de Student"):
        st.markdown("**Hipóteses:**")
        st.latex(r"H_0: \mu_E \leq \mu_A \quad \text{(Eletricistas têm produtividade igual ou menor que ajudantes)}")
        st.latex(r"H_1: \mu_E > \mu_A \quad \text{(Eletricistas têm produtividade maior)}")

        st.markdown("**Fórmula da estatística t:**")
        st.latex(r"t = \frac{\bar{X}_E - \bar{X}_A}{s_p \cdot \sqrt{\frac{1}{n_E} + \frac{1}{n_A}}}")

        st.markdown("**Onde:**")
        st.latex(r"s_p^2 = \frac{(n_E - 1)s_E^2 + (n_A - 1)s_A^2}{n_E + n_A - 2}")

        st.markdown("""
        O valor-p indica a probabilidade de obter esse resultado caso H₀ seja verdadeira.  
        Se for menor que **0.05**, rejeitamos H₀ e concluímos que eletricistas são mais produtivos.
        """)

    stat, p_value = ttest_ind(eletricista_ip, ajudante_ip, equal_var=True)
    st.write(f"**Estatística t:** {stat:.3f}")
    st.write(f"**Valor-p:** {p_value:.4f}")

    if p_value <= 0.05:
        st.success("Rejeitamos H₀: Existe evidência de que eletricistas são mais produtivos que ajudantes.")
    else:
        st.info("Não rejeitamos H₀: Não há evidência suficiente para afirmar que eletricistas são mais produtivos.")

    st.markdown("""
        **Entendendo o resultado:**

        - A estatística **t** mede o quão distante está a média dos eletricistas da média dos ajudantes em termos de erro padrão.
        - O **valor t** quantifica a diferença em **unidades de erro padrão**.
        - O **valor-p** representa a **probabilidade de observar uma diferença tão grande (ou maior)** entre os grupos, **assumindo que a hipótese nula (H₀) é verdadeira**.
        - Se o valor-p for menor que 0.05, **rejeitamos H₀** e dizemos que a diferença é estatisticamente significativa.

        """, unsafe_allow_html=True)


    st.markdown("""<h4>Resultado do Teste U de Mann-Whitney</h4>""", unsafe_allow_html=True)

    with st.expander("Explicação do Teste U de Mann-Whitney"):
        st.markdown(r"""
        O teste de Mann-Whitney é uma alternativa não paramétrica ao teste t de Student, usada quando os dados não seguem uma distribuição normal.

        Ele compara as posições (ranks) das observações, e não as médias diretamente.

        É útil quando:
        - Os dados não seguem distribuição normal
        - As variâncias são diferentes
        - Existem outliers
        """)

    u_stat, u_p = mannwhitneyu(eletricista_ip, ajudante_ip, alternative='greater')
    st.write(f"**Estatística U:** {u_stat:.3f}")
    st.write(f"**Valor-p:** {u_p:.4f}")

    if u_p <= 0.05:
        st.success("Rejeitamos H₀: Eletricistas têm produtividade maior (teste Mann-Whitney).")
    else:
        st.info("Não rejeitamos H₀: Não há diferença significativa (teste Mann-Whitney).")

    st.markdown("""
        **Entendendo o resultado:**

        - A estatística **U** mede a frequência com que os valores de um grupo (eletricistas) **excedem os valores** do outro grupo (ajudantes), considerando todas as comparações possíveis entre os dois grupos.
        - O **teste U de Mann-Whitney** é uma alternativa **não paramétrica** ao teste t. Ele é usado quando **não podemos assumir normalidade** ou **quando há presença de outliers**.
        - O **valor-p** indica a **probabilidade de obter a distribuição observada (ou mais extrema)** sob a hipótese nula de que os grupos têm **produtividades iguais**.

        """, unsafe_allow_html=True)

else:
    st.warning("Não foram encontrados dados suficientes de 'ELETRICISTA (SGSP)' e 'AJUDANTE (SGSP)' para 'INSTALACOES ELETRICAS'.")
    
st.subheader("Conclusão Final")

st.write("Com base nos testes realizados para comparar a produtividade entre eletricistas e ajudantes, podemos concluir que não há evidência estatística suficiente para afirmar que os eletricistas são mais produtivos do que os ajudantes.")
st.write("Utilizando o teste t de Student, que compara as médias das duas amostras, obtivemos um valor-p de 0.1723, que é maior que o nível de significância de 5%. Isso indica que não podemos rejeitar a hipótese nula, ou seja, não há uma diferença significativa na produtividade entre os dois grupos.")
st.write("Além disso, o teste U de Mann-Whitney, uma alternativa não paramétrica ao teste t, também resultou em um valor-p de 0.1439, o que reforça a conclusão de que não há uma diferença estatisticamente significativa entre a produtividade dos eletricistas e dos ajudantes.")
st.write("Portanto, com base nos resultados de ambos os testes, não podemos afirmar que os eletricistas apresentam uma produtividade superior à dos ajudantes nas obras analisadas. Isso sugere que, sob as condições analisadas, a produtividade entre os dois grupos é comparável, e não há uma diferença substancial entre eles.")

