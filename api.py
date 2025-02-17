from fastapi import FastAPI
from pydantic import BaseModel
import pickle
from prophet import Prophet
import pandas as pd
import requests
import io

app = FastAPI()

url = 'https://raw.githubusercontent.com/Baaprado/Pos_Tech_FIAP_Fase_4/main/modelo_prophet.pkl'

try:
    response = requests.get(url)
    response.raise_for_status()  

    if len(response.content) == 0:
        raise ValueError("O arquivo baixado está vazio.")

    with io.BytesIO(response.content) as f:
        modelo_prophet = pickle.load(f)
    print("Modelo carregado com sucesso!")
except Exception as e:
    print(f"Erro ao carregar o modelo: {e}")
    modelo_prophet = None  

class PredictRequest(BaseModel):
    dias: int

@app.post("/predict")
def predict(request: PredictRequest):
    if modelo_prophet is None:
        return {"error": "Modelo não carregado. Verifique o arquivo .pkl."}

    dias = request.dias  

    future = modelo_prophet.make_future_dataframe(periods=dias, freq='D')
    forecast = modelo_prophet.predict(future)
    
    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(dias).to_dict(orient='records')