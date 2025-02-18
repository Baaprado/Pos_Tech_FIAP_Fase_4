import streamlit as st
import pickle
import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet
import requests
import io

st.set_page_config(page_title="Previsão do Preço do Petróleo Brent", page_icon="🛢️", layout="wide")

st.title("Previsão do Preço do Petróleo Brent com Prophet 🛢️")

st.sidebar.title("Sobre o Projeto")
st.sidebar.markdown("""
**Problema:**
Você foi contratado(a) para uma consultoria, e seu trabalho envolve analisar os dados de preço do petróleo Brent, que pode ser encontrado no site do IPEA. Essa base de dados histórica envolve duas colunas: data e preço (em dólares). Um grande cliente do segmento pediu para que a consultoria desenvolvesse um dashboard interativo para gerar insights relevantes para tomada de decisão. Além disso, solicitaram que fosse desenvolvido um modelo de Machine Learning para fazer o forecasting do preço do petróleo.

**Objetivo:**
- Criar um dashboard interativo com ferramentas à sua escolha.
- Desenvolver um modelo de Machine Learning para previsão diária do preço do petróleo.
- Fazer o deploy do modelo em produção e criar um MVP utilizando o Streamlit.
""")

st.header("Carregando o Modelo Prophet")
url = 'https://raw.githubusercontent.com/Baaprado/Pos_Tech_FIAP_Fase_4/main/modelo_prophet.pkl'

try:
    response = requests.get(url)
    response.raise_for_status() 

    with io.BytesIO(response.content) as f:
        modelo_prophet = pickle.load(f)
    st.success("Modelo carregado com sucesso!")
except Exception as e:
    st.error(f"Erro ao carregar o modelo: {e}")
    modelo_prophet = None  

st.header("O que é o Prophet?")
st.markdown("""
O **Prophet** é uma ferramenta de forecasting desenvolvida pelo Facebook (agora Meta) para prever séries temporais. Ele é especialmente útil para dados com padrões sazonais, tendências e feriados. O Prophet é fácil de usar e requer pouca configuração, tornando-o ideal para previsões rápidas e precisas.

Neste projeto, utilizamos o Prophet para prever o preço do petróleo Brent com base em dados históricos.
""")

st.header("Insights sobre o Preço do Petróleo Brent")
st.markdown("""
Aqui estão alguns insights relevantes sobre a variação do preço do petróleo Brent:

1. **Impacto de Crises Geopolíticas:**
   - Eventos como conflitos no Oriente Médio ou sanções a grandes produtores de petróleo (como Rússia e Irã) podem causar picos significativos no preço do petróleo.

2. **Crises Econômicas Globais:**
   - Durante recessões econômicas, a demanda por petróleo tende a cair, resultando em quedas nos preços. Por exemplo, a crise financeira de 2008 e a pandemia de COVID-19 em 2020.

3. **Demanda Global por Energia:**
   - O aumento da demanda por energia, especialmente em economias emergentes como China e Índia, pode pressionar os preços do petróleo para cima.

4. **Transição Energética:**
   - A crescente adoção de energias renováveis e veículos elétricos pode reduzir a demanda por petróleo a longo prazo, impactando os preços.
""")

st.sidebar.header("Configurações de Previsão")
dias_previsao = st.sidebar.number_input("Número de Dias para Previsão", value=365, min_value=1)

if st.sidebar.button("Prever"):
    if modelo_prophet is None:
        st.error("Modelo não carregado. Verifique o arquivo .pkl.")
    else:
        future = modelo_prophet.make_future_dataframe(periods=dias_previsao, freq='D')
        forecast = modelo_prophet.predict(future)

        st.header("Previsão do Preço do Brent")
        st.write(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(dias_previsao))

        st.header("Gráfico de Previsão")
        fig, ax = plt.subplots(figsize=(12, 6))
        modelo_prophet.plot(forecast, ax=ax)
        plt.xlabel("Data")
        plt.ylabel("Preço do Brent (USD)")
        plt.title("Previsão do Preço do Petróleo Brent")
        st.pyplot(fig)

st.markdown("---")
st.markdown("""
**Desenvolvido por:** [Barbara Rodrigues Prado e Edvaldo Torres]  
**Fonte dos dados:** IPEA  
**Ferramentas utilizadas:** Python, Streamlit, Prophet  
**Repositório do projeto:** [GitHub](https://github.com/Baaprado/Pos_Tech_FIAP_Fase_4)
""")