# Pos_Tech_FIAP_Fase_4

Passos do projeto:

1. Extração, tratamento e análise exploratória dos dados do ipea no arquivo ˜Analise_e_Modelos_Preço_do_Petróleo.ipynb˜
2. Criação de um dashboard interativo via Streamlit no arquivo "Dashboard_Petroleo.py"
3. Testes e criação do modelo no arquivo "Analise_e_Modelos_Preço_do_Petróleo.ipynb"
4. Criação do arquivo "modelo_prophet.pkl"
5. Criação da API via FastAPI no arquivo "api.py"
6. Criação de um app para interação com o modelo no arquivo "app.py"

Instruções:

1. Executar o notebook ˜Analise_e_Modelos_Preço_do_Petróleo.ipynb˜ para visualização do tratamento dos dados e das análises realizadas
2. Executar o arquivo "Dashboard_Petroleo.py" e inserir o comando "streamlit run Dashboard_Petroleo.py" no terminal para acessar o dashboard
3. Para acessar e interagir com o modelo, no terminal:
   - Faça um clone do repositório atual: git clone https://github.com/Baaprado/Pos_Tech_FIAP_Fase_4.git
   - Navegue até o diretório: cd Pos_Tech_FIAP_Fase_4
   - Instale as dependências: pip install streamlit pandas matplotlib prophet requests
   - Execute o app.py: streamlit run app.py

O problema:

Você foi contratado(a) para uma consultoria, e seu trabalho envolve
analisar os dados de preço do petróleo brent, que pode ser encontrado no site
do ipea. Essa base de dados histórica envolve duas colunas: data e preço (em
dólares). Um grande cliente do segmento pediu para que a consultoria
desenvolvesse um dashboard interativo para gerar insights relevantes para
tomada de decisão. Além disso, solicitaram que fosse desenvolvido um modelo
de Machine Learning para fazer o forecasting do preço do petróleo.

Seu objetivo é:

• Criar um dashboard interativo com ferramentas à sua escolha.

• Seu dashboard deve fazer parte de um storytelling que traga insights
relevantes sobre a variação do preço do petróleo, como situações
geopolíticas, crises econômicas, demanda global por energia e etc. Isso
pode te ajudar com seu modelo. É obrigatório que você traga pelo menos
4 (quatro) insights neste desafio.

• Criar um modelo de Machine Learning que faça a previsão do preço do
petróleo diariamente (lembre-se de time series). Esse modelo deve estar
contemplado em seu storytelling e deve conter o código que você
trabalhou, analisando as performances do modelo.

• Criar um plano para fazer o deploy em produção do modelo, com as
ferramentas que são necessárias.

• Faça um MVP do seu modelo em produção utilizando o Streamlit.
