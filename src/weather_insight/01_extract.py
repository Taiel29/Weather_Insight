import requests
from pymongo import MongoClient
from datetime import datetime

url = "https://api.open-meteo.com/v1/forecast"

params = {
	"latitude": -34.608056,
	"longitude": -58.370278,
	"hourly": ["temperature_2m", "precipitation_probability", "precipitation", "wind_speed_10m", "visibility"],
	"timezone": "America/Sao_Paulo",
}

try:
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    datos = r.json()

except requests.exceptions.RequestException as e:
    print(f"No se pudo obtener el clima: {e}")
    datos = None

if datos:
    client = MongoClient("mongodb://localhost:27017")
    db = client["WeatherInsight"]
    collection = db["weather_raw"]

    documento = {
        "fecha_descarga": datetime.now(),
        "fuente": "Open-Meteo",
        "datos": datos
    }

    resultado = collection.insert_one(documento)

    print(f"Documento guardado: {resultado.inserted_id}")

    client.close()