import requests
from pymongo import MongoClient
from datetime import datetime
from weather_insight.config import (
    API_URL,
    LATITUDE,
    LONGITUDE,
    MONGO_COLLECTION,
    MONGO_DATABASE,
    MONGODB_URI,
    TIMEZONE,
)

def extract_weather():
    url = API_URL

    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "hourly": ["temperature_2m", "precipitation_probability", "precipitation", "wind_speed_10m", "visibility"],
        "timezone": TIMEZONE,
    }

    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()

    except requests.exceptions.RequestException as e:
        print(f"No se pudo obtener el clima: {e}")
        data = None

    if data:
        client = MongoClient(MONGODB_URI)
        db = client[MONGO_DATABASE]
        collection = db[MONGO_COLLECTION]

        documento = {
            "download_date": datetime.now(),
            "source": "Open-Meteo",
            "data": data
        }

        response = collection.insert_one(documento)

        print(f"Documento guardado: {response.inserted_id}")

        client.close()