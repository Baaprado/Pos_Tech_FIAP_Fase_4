import streamlit as st
import pickle
import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet
import requests
import io

st.title("Previsão do Preço do Petróleo Brent com Prophet")

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

st.sidebar.header("Configurações de Previsão")
dias_previsao = st.sidebar.number_input("Número de Dias para Previsão", value=365, min_value=1)

if st.sidebar.button("Prever"):
    if modelo_prophet is None:
        st.error("Modelo não carregado. Verifique o arquivo .pkl.")
    else:
        future = modelo_prophet.make_future_dataframe(periods=dias_previsao, freq='D')
        forecast = modelo_prophet.predict(future)

        st.subheader("Previsão do Preço do Brent")
        st.write(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(dias_previsao))

        st.subheader("Gráfico de Previsão")
        fig, ax = plt.subplots(figsize=(12, 6))
        modelo_prophet.plot(forecast, ax=ax)
        plt.xlabel("Data")
        plt.ylabel("Preço do Brent (USD)")
        plt.title("Previsão do Preço do Petróleo Brent")
        st.pyplot(fig)