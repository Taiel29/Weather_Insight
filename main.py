import requests
import pandas as pd

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
    hourly = datos["hourly"]
    df = pd.DataFrame(hourly)

    df["time"] = pd.to_datetime(df["time"])
    df = df.dropna()

    df.to_csv("observacion.csv", index=False)