import streamlit as st
import pickle
import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet
import requests
import io

st.set_page_config(page_title="Previsão do Preço do Petróleo Brent", layout="wide")

st.title("Previsão do Preço do Petróleo Brent com Prophet")

st.sidebar.title("Sobre o Projeto")
st.sidebar.markdown("""
**Problema:**
Você foi contratado(a) para analisar os dados históricos do preço do petróleo Brent, disponíveis no site do IPEA, 
e desenvolver um dashboard interativo para gerar insights relevantes para a tomada de decisão de um cliente.
Além disso, é necessário criar um modelo de Machine Learning para previsão diária do preço do petróleo, 
realizar o deploy do modelo em produção e criar um MVP utilizando o Streamlit.
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

1. **Pandemia:**
   - Colapso da demanda global devido a pandemia de COVID-19 e as medidas de lockdown em diversos países levaram a uma drástica redução na demanda por petróleo, impactando diretamente os preços.
   - No início de 2020, uma disputa entre a Arábia Saudita e a Rússia sobre cortes na produção de petróleo resultou em uma guerra de preços, com ambos os países aumentando sua produção e derrubando ainda mais os preços.
   - Diante da crise, a OPEP+ (Organização dos Países Exportadores de Petróleo e aliados) firmou um acordo histórico de corte na produção, buscando estabilizar os preços e evitar um colapso ainda maior.
   - Após os choques iniciais, o mercado de petróleo iniciou uma recuperação gradual, impulsionada pela retomada da atividade econômica em alguns países e pelos cortes na produção da OPEP+.

2. **Recuperação e Crescimento da Demanda:**
   - Com o avanço da vacinação contra a COVID-19 e a flexibilização das restrições, a demanda global por petróleo começou a se recuperar gradualmente em 2021.
   - A OPEP+ gradualmente aumentou sua produção ao longo de 2021 para atender à crescente demanda, mas manteve alguns cortes em vigor para evitar uma queda nos preços.
   - No final de 2021, a Europa enfrentou uma crise energética devido à escassez de gás natural, o que também afetou o mercado de petróleo, impulsionando a demanda por combustíveis alternativos.

3. **Conflito Rússia x Ucrânia e Decisões da OPEP:**
   - O conflito desencadeado pela invasão russa gerou uma crise energética global, com sanções e incertezas sobre o fornecimento de petróleo russo, impulsionando os preços para patamares elevados.
   - A OPEP+ manteve sua estratégia de produção controlada, buscando equilibrar o mercado e evitar uma queda nos preços, o que contribuiu para a alta do petróleo.
   - A recuperação pós-pandemia perdeu força, com a desaceleração do crescimento global, especialmente na China, gerando preocupações sobre a demanda futura por petróleo.
   - A alta da inflação global e as políticas monetárias restritivas adotadas por diversos países, como o aumento das taxas de juros, também afetaram o mercado de petróleo, influenciando a demanda e os preços.

4. **Estabilidade e Transição Energética:**
   - Após a alta volatilidade em 2022, os preços do petróleo se estabilizaram em 2023, oscilando em uma faixa mais estreita.
   - A crescente preocupação com as mudanças climáticas e a transição para fontes de energia mais limpas influenciaram o mercado de petróleo, com debates sobre o futuro do setor e investimentos em energias renováveis.
   - Os Estados Unidos aumentaram sua produção de petróleo em 2023, tornando-se um dos principais produtores globais e influenciando os preços.

5. **Continuação da Transição e Geopolítica:**
   - A transição para energias renováveis continuou a ser um tema central em 2024, com diversos países e empresas estabelecendo metas de redução de emissões e investindo em tecnologias limpas.
   - Conflitos regionais e tensões geopolíticas em diversas partes do mundo continuaram a ser um fator de risco para o mercado de petróleo, com potencial para afetar a produção e distribuição.
   - O mercado de petróleo manteve um olhar atento à demanda global, especialmente na China, que é um dos maiores consumidores de petróleo do mundo.
""")

st.sidebar.header("Configurações de Previsão")
dias_previsao = st.sidebar.number_input("Número de Dias para Previsão", value=365, min_value=1)

if st.sidebar.button("Prever"):
    if modelo_prophet is None:
        st.error("Modelo não carregado. Verifique o arquivo .pkl.")
    else:
        future = modelo_prophet.make_future_dataframe(periods=dias_previsao, freq='D')
        forecast = modelo_prophet.predict(future)

        forecast_renamed = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].rename(columns={
            'ds': 'Data',
            'yhat': 'Preço Previsto (USD)',
            'yhat_lower': 'Limite Inferior',
            'yhat_upper': 'Limite Superior'
        })

        st.header("Previsão do Preço do Brent")
        st.write(forecast_renamed.tail(dias_previsao))  # Exibindo as previsões com os novos nomes de coluna

        st.header("Gráfico de Previsão")
        fig, ax = plt.subplots(figsize=(12, 6))
        modelo_prophet.plot(forecast, ax=ax)
        plt.xlabel("Data")
        plt.ylabel("Preço do Brent (USD)")
        plt.title("Previsão do Preço do Petróleo Brent")
        st.pyplot(fig)

st.markdown("---")
st.markdown("""
**Trabalho:** Fase 4 do curso de Data Analytics da Pós Tech FIAP
            
**Desenvolvido por:** Barbara Rodrigues Prado RM357381 e Edvaldo Torres RM357417
            
**Fonte dos dados:** IPEA  
            
**Ferramentas utilizadas:** Python, Streamlit  
            
**Repositório do projeto:** [GitHub](https://github.com/Baaprado/Pos_Tech_FIAP_Fase_4)
""")