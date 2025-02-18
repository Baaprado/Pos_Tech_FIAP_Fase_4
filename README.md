# Pos_Tech_FIAP_Fase_4

## Visão Geral

Este projeto tem como objetivo analisar dados históricos do preço do petróleo Brent, construir um dashboard interativo e desenvolver um modelo de previsão utilizando Machine Learning. O modelo é integrado a uma API e um aplicativo para interação via Streamlit.

## Estrutura do Projeto

1. **Extração, tratamento e análise exploratória** dos dados do IPEA no arquivo [`Analise_e_Modelos_Preço_do_Petróleo.ipynb`](Analise_e_Modelos_Preço_do_Petróleo.ipynb).
2. **Criação de um dashboard interativo** via Streamlit no arquivo [`Dashboard_Petroleo.py`](Dashboard_Petroleo.py).
3. **Desenvolvimento do modelo de previsão** no arquivo [`Analise_e_Modelos_Preço_do_Petróleo.ipynb`](Analise_e_Modelos_Preço_do_Petróleo.ipynb).
4. **Geração do arquivo do modelo treinado** (`modelo_prophet.pkl`).
5. **Criação da API** utilizando FastAPI no arquivo [`api.py`](api.py).
6. **Desenvolvimento de um aplicativo** para interação com o modelo via Streamlit no arquivo [`app.py`](app.py).

---

## Como Executar

Clone este repositório e navegue até o diretório do projeto:
```sh
git clone https://github.com/Baaprado/Pos_Tech_FIAP_Fase_4.git
cd Pos_Tech_FIAP_Fase_4
```

Instale as dependências necessárias:
```sh
pip install streamlit pandas matplotlib prophet requests
```

Execute o aplicativo interativo:
```sh
streamlit run app.py
```

Execute o dashboard interativo:
```sh
streamlit run Dashboard_Petroleo.py
```

---

## Sobre o Problema

Você foi contratado(a) para uma consultoria e recebeu a missão de analisar os dados históricos do preço do petróleo Brent, disponíveis no site do IPEA. A base de dados contém duas colunas: **data** e **preço (em dólares)**. 

Um grande cliente do setor solicitou um **dashboard interativo** para fornecer insights sobre a variação do preço do petróleo. Além disso, também requisitou um **modelo de Machine Learning** para prever os preços futuros do petróleo.

### Objetivos do Projeto

- Criar um **dashboard interativo** utilizando ferramentas adequadas.
- Integrar o dashboard em um **storytelling** com insights relevantes sobre variações no preço do petróleo (ex: impactos geopolíticos, crises econômicas, demanda global de energia, etc.).
- Desenvolver um **modelo de Machine Learning para previsão de preços** considerando séries temporais.
- Analisar e documentar a performance do modelo.
- Criar um **plano de deploy** para disponibilizar o modelo em produção.
- Implementar um **MVP do modelo** usando Streamlit para interação com o usuário final.

---

## Tecnologias Utilizadas

- **Linguagem**: Python
- **Bibliotecas**: Pandas, Matplotlib, Prophet, FastAPI, Streamlit, Requests
- **Ferramentas**: Jupyter Notebook, VSCode, Google Colab

Caso tenha dúvidas ou queira contribuir com o projeto, sinta-se à vontade para abrir uma issue ou pull request!

---


📌 Desenvolvido por [Barbara Prado e Edvaldo Torres](https://github.com/Baaprado)
