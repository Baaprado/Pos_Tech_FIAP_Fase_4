import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import requests
from io import StringIO

st.set_page_config(layout="wide")

url = 'https://drive.google.com/uc?id=1ilAXCcKolm_2WAVdiC_1ycQTq5zHMwhj'  
response = requests.get(url)
response.raise_for_status()  

csv_data = StringIO(response.text)
df = pd.read_csv(csv_data, sep=';', decimal=',')
df = df.drop(df.columns[2], axis=1)
df.columns = ['DAT_MEDICAO', 'VLR_PRECO_PRETROLEO_BRUTO_DOLAR_BRENT']
df['DAT_MEDICAO'] = pd.to_datetime(df['DAT_MEDICAO'])
df = df[df['DAT_MEDICAO'] >= '2020-01-01'].reset_index(drop=True)
df_tratado = df.copy()
df_tratado = df_tratado.dropna().reset_index(drop=True)
df_tratado['DAT_MES_MEDICAO'] = df_tratado['DAT_MEDICAO'].dt.strftime('%Y-%m')
df_tratado['NUM_DIA_SEMANA'] = df_tratado['DAT_MEDICAO'].dt.dayofweek
df_tratado['NUM_ANO'] = df_tratado['DAT_MEDICAO'].dt.year
df_tratado['NME_MES'] = df_tratado['DAT_MEDICAO'].dt.strftime("%b")
df_tratado = df_tratado[(df_tratado['NUM_ANO'] >= 2020) & (df_tratado['NUM_ANO'] <= 2024)]
df_tratado = df_tratado[['DAT_MEDICAO', 'DAT_MES_MEDICAO', 'NUM_DIA_SEMANA', 'NME_MES', 'NUM_ANO', 'VLR_PRECO_PRETROLEO_BRUTO_DOLAR_BRENT']]
df_tratado = df_tratado[['DAT_MEDICAO','DAT_MES_MEDICAO','NUM_DIA_SEMANA','NME_MES','NUM_ANO','VLR_PRECO_PRETROLEO_BRUTO_DOLAR_BRENT']]

min_data = df_tratado['DAT_MEDICAO'].min().date()
max_data = df_tratado['DAT_MEDICAO'].max().date()
anos_disponiveis = sorted(df_tratado['NUM_ANO'].unique())
anos_disponiveis = [ano for ano in anos_disponiveis if ano not in [2019, 2025]]

anos_selecionados = st.sidebar.multiselect("Selecione os anos", options=anos_disponiveis, default=anos_disponiveis)
ano_mes_inicio = st.sidebar.date_input('Data início', value=min_data, min_value=min_data, max_value=max_data)
ano_mes_fim = st.sidebar.date_input('Data fim', value=max_data, min_value=min_data, max_value=max_data)

ano_mes_inicio = pd.to_datetime(ano_mes_inicio)
ano_mes_fim = pd.to_datetime(ano_mes_fim)

df_filtrado = df_tratado[(df_tratado['DAT_MEDICAO'] >= ano_mes_inicio) & (df_tratado['DAT_MEDICAO'] <= ano_mes_fim)]

if anos_selecionados:
    df_filtrado = df_filtrado[df_filtrado['NUM_ANO'].isin(anos_selecionados)]

# Gráficos do Dashboard

fig1 = px.line(df_filtrado, 
                x='DAT_MEDICAO', 
                y='VLR_PRECO_PRETROLEO_BRUTO_DOLAR_BRENT', 
                title='Série Temporal do Preço do Petróleo Bruto (Brent)',
                markers= True,
                color='NUM_ANO',
                labels={'NUM_ANO': 'Anos'}
                )
fig1.update_layout(xaxis_title='Data de Medição', 
                   yaxis_title='Preço do Petróleo (USD)', 
                   template='plotly_dark') 


fig2 = px.box(df_filtrado, 
             x="NME_MES", 
             y="VLR_PRECO_PRETROLEO_BRUTO_DOLAR_BRENT",
             title="Variação do Preço do Petróleo Brent ao longo dos meses",
             labels={"DAT_MES_MEDICAO": "Mês", "VLR_PRECO_PRETROLEO_BRUTO_DOLAR_BRENT": "Preço do Petróleo (USD)"}
             )

fig2.update_layout(xaxis_title='Comportamento por mês')  

fig3 = px.histogram(df_filtrado, 
                   x="VLR_PRECO_PRETROLEO_BRUTO_DOLAR_BRENT", 
                   nbins=30,  
                   title="Histograma da Distribuição de Preços do Petróleo Brent",
                   labels={"VLR_PRECO_PRETROLEO_BRUTO_DOLAR_BRENT": "Preço do Petróleo (USD)"},
                   color_discrete_sequence=["royalblue"])

fig3.update_layout(bargap=0.1)  

fig4 = px.line(df_filtrado.groupby('DAT_MES_MEDICAO').last().reset_index(), 
                x='NME_MES', 
                y='VLR_PRECO_PRETROLEO_BRUTO_DOLAR_BRENT', 
                title='Fechamento mensal do Preço do Petróleo Bruto (Brent)',
                markers= True,
                color='NUM_ANO',
                labels={'NUM_ANO': 'Anos'}
                )
fig4.update_layout(xaxis_title='Data de Medição', 
                   yaxis_title='Preço do Petróleo (USD)', 
                   template='plotly_dark') 

# Exibir no Streamlit

st.title("Fase 4 - Tech Challenge - Análise de Pretróleo Bruto")

st.markdown('''
            Este dashboard tem como objetivo fornecer uma visão abrangente do mercado global de petróleo bruto nos últimos cinco anos (2020-2024), utilizando como referência o preço do petróleo Brent, um dos principais indicadores do mercado. O petróleo Brent é um tipo de petróleo bruto extraído no Mar do Norte, amplamente utilizado como referência para precificar o petróleo em diversas regiões do mundo. Abaixo, apresentamos gráficos que ilustram a evolução e a variação dos preços ao longo desse período, permitindo uma análise mais detalhada das tendências do setor.
            ''')

st.header("Último cenário atualizado")
met1,met2,met3, met4, met5 = st.columns(5)
with met1:
    st.metric("Última modificação da base", df_tratado['DAT_MEDICAO'].max().strftime('%d/%m/%Y'))
with met2:
    st.metric("Último Preço Pretróleo", f"${df_tratado[df_tratado['DAT_MEDICAO']==df_tratado['DAT_MEDICAO'].max()]['VLR_PRECO_PRETROLEO_BRUTO_DOLAR_BRENT'].sum():,.2f}")
with met3:
    st.metric("Valor Médio do Ultimo Ano", f"${df_tratado[df_tratado['NUM_ANO'] == df_tratado['NUM_ANO'].max() - 1]['VLR_PRECO_PRETROLEO_BRUTO_DOLAR_BRENT'].mean():,.2f}")


st.header("Análise temporal do preço do petróleo")

st.plotly_chart(fig1) 

st.markdown('''
            O gráfico mostra a variação do preço do petróleo Brent entre 2020 e 2024, destacando uma forte queda em 2020 devido à pandemia de COVID-19, que impactou drasticamente a demanda global por petróleo. Em 2021, 
            observamos uma recuperação gradual dos preços, impulsionada pela retomada da atividade econômica. Em 2022, o mercado experimentou alta volatilidade, com um pico acima de 120 USD, impulsionado por eventos geopolíticos 
            como a guerra na Ucrânia, que gerou incertezas sobre o fornecimento de petróleo. Nos anos seguintes, o preço passou por um declínio e estabilização, oscilando entre 70 e 90 USD.
            ''')

st.plotly_chart(fig4)
st.markdown('''
            Os preços do petróleo Brent apresentam padrões sazonais, com variações significativas ao longo do ano, como o aumento observado em 2022 até meados do ano, seguido por uma queda gradual. 
            Essa sazonalidade pode ser influenciada por fatores como a demanda sazonal por combustíveis (por exemplo, maior demanda no inverno para aquecimento) e fatores climáticos que podem afetar a produção e distribuição de petróleo. 
            A comparação entre anos revela que 2022 teve os preços mais altos, enquanto 2020 sofreu uma forte queda a partir de março, refletindo o impacto da pandemia de COVID-19. A partir de 2023, os preços se estabilizaram na faixa de 70 a 90 USD, 
            indicando menor volatilidade após as crises econômicas e geopolíticas. 2020 se destaca como um ponto fora da curva, com uma queda abrupta nos primeiros meses, sem precedentes nos outros anos analisados.
            ''')

col2, col3 = st.columns(2)
with col2:
    st.plotly_chart(fig2, use_container_width=True)
with col3:
    st.plotly_chart(fig3, use_container_width=True)

st.markdown('''
            A análise da volatilidade dos preços do petróleo Brent revela que meses como Fevereiro e Março (no período completo analisado) tendem a apresentar maior volatilidade, enquanto meses como Novembro e Dezembro (no mesmo período) costumam ser mais estáveis. 
            A presença de outliers significativos, como o pico de preço em 2022, reforça a ideia de que eventos extremos, como a guerra na Ucrânia, ocorreram nesse período e impactaram os preços. A distribuição dos preços nos últimos 5 anos mostra que a faixa de 70 a 90 USD é a mais comum, 
            representando a maior parte das ocorrências.
            ''')
st.header(" Historico de Eventos")
with st.expander('2020 - Pandemia'):
    st.markdown(''' 
                - Colapso da demanda global devido a pandemia de COVID-19 e as medidas de lockdown em diversos países levaram a uma drástica redução na demanda por petróleo, impactando diretamente os preços.
                - No início de 2020, uma disputa entre a Arábia Saudita e a Rússia sobre cortes na produção de petróleo resultou em uma guerra de preços, com ambos os países aumentando sua produção e derrubando ainda mais os preços.
                - Diante da crise, a OPEP+ (Organização dos Países Exportadores de Petróleo e aliados) firmou um acordo histórico de corte na produção, buscando estabilizar os preços e evitar um colapso ainda maior.
                - Após os choques iniciais, o mercado de petróleo iniciou uma recuperação gradual, impulsionada pela retomada da atividade econômica em alguns países e pelos cortes na produção da OPEP+.
                ''')
with st.expander('2021 - Recuperação e Crescimento da Demanda'):
    st.markdown(''' 
                - Com o avanço da vacinação contra a COVID-19 e a flexibilização das restrições, a demanda global por petróleo começou a se recuperar gradualmente em 2021.
                - A OPEP+ gradualmente aumentou sua produção ao longo de 2021 para atender à crescente demanda, mas manteve alguns cortes em vigor para evitar uma queda nos preços.
                - No final de 2021, a Europa enfrentou uma crise energética devido à escassez de gás natural, o que também afetou o mercado de petróleo, impulsionando a demanda por combustíveis alternativos.
                ''')
with st.expander('2022 - Conflito Rússia x Ucrânia e Decisões da OPEP'):
    st.markdown('''
                - O conflito desencadeado pela invasão russa gerou uma crise energética global, com sanções e incertezas sobre o fornecimento de petróleo russo, impulsionando os preços para patamares elevados.
                - A OPEP+ manteve sua estratégia de produção controlada, buscando equilibrar o mercado e evitar uma queda nos preços, o que contribuiu para a alta do petróleo.
                - A recuperação pós-pandemia perdeu força, com a desaceleração do crescimento global, especialmente na China, gerando preocupações sobre a demanda futura por petróleo.
                - A alta da inflação global e as políticas monetárias restritivas adotadas por diversos países, como o aumento das taxas de juros, também afetaram o mercado de petróleo, influenciando a demanda e os preços.
                ''')
with st.expander('2023 - Estabilidade e Transição Energética'):
    st.markdown(''' 
                - Após a alta volatilidade em 2022, os preços do petróleo se estabilizaram em 2023, oscilando em uma faixa mais estreita.
                - A crescente preocupação com as mudanças climáticas e a transição para fontes de energia mais limpas influenciaram o mercado de petróleo, com debates sobre o futuro do setor e investimentos em energias renováveis.
                - Os Estados Unidos aumentaram sua produção de petróleo em 2023, tornando-se um dos principais produtores globais e influenciando os preços.
                ''')

with st.expander('2024 - Continuação da Transição e Geopolítica'):
    st.markdown(''' 
                - A transição para energias renováveis continuou a ser um tema central em 2024, com diversos países e empresas estabelecendo metas de redução de emissões e investindo em tecnologias limpas.
                - Conflitos regionais e tensões geopolíticas em diversas partes do mundo continuaram a ser um fator de risco para o mercado de petróleo, com potencial para afetar a produção e distribuição.
                - O mercado de petróleo manteve um olhar atento à demanda global, especialmente na China, que é um dos maiores consumidores de petróleo do mundo.
                ''')

st.header(" Conclusão de dados")
st.markdown('''
            Concluindo, o dashboard apresentado oferece uma análise abrangente do mercado de petróleo bruto nos últimos cinco anos, focando na evolução do preço do petróleo Brent. Os gráficos exibidos ilustram a volatilidade do mercado, influenciado por eventos como a pandemia de COVID-19 em 2020 e eventos geopolíticos em 2022.   

            A análise revela que o mercado de petróleo Brent é suscetível a flutuações significativas, com períodos de alta volatilidade, como Fevereiro e Março, e outros de maior estabilidade, como Novembro e Dezembro. Os preços têm oscilado principalmente entre 70 e 90 USD nos últimos anos, com 2020 sendo um ano atípico devido à pandemia.
            ''')

st.markdown("---")
st.markdown("""
**Trabalho desenvolvido para a Fase 4 da Pós Tech FIAP**
**Desenvolvido por:** Barbara Rodrigues Prado RM357381 e Edvaldo Torres RM357417
**Fonte dos dados:** IPEA  
**Ferramentas utilizadas:** Python, Streamlit  
**Repositório do projeto:** [GitHub](https://github.com/Baaprado/Pos_Tech_FIAP_Fase_4)
""")