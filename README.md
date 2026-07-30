# Weather Insight

Pipeline ETL en Python que recopila datos meteorológicos desde una API pública, los procesa y almacena en MongoDB y SQL Server, y los expone en dashboards de Power BI. Automatizado con Docker y cron para mantener un historial sin intervención manual.

## Por qué este proyecto

Proyecto de portfolio orientado a roles de datos, con foco en decisiones de diseño de un pipeline (manejo de errores, tolerancia a cambios de esquema, idempotencia).

## Arquitectura

```
Open-Meteo API
      │
      ▼
  extract.py  ──────────► raw_store.py ──────► MongoDB
      │                                         (capa de datos crudos)
      ▼
transform.py  ◄─────────────────────────────────┘
      │
      ▼
   load.py ────────────────────────────────► SQL Server
      │
      ▼
   Power BI (dashboards)
```

El pipeline completo se disparará cada 1 hora vía cron dentro de un contenedor Docker.

## Stack

- **Python** — lenguaje del pipeline
- **requests** — consumo de la API de Open-Meteo
- **pandas** — limpieza y transformación
- **MongoDB** (pymongo) — capa de datos crudos
- **SQL Server** (SQLAlchemy) — almacenamiento relacional para análisis
- **Docker** — ejecución reproducible
- **cron** — orquestación periódica (cada 1 hora)
- **Power BI** — dashboards

## Decisiones de diseño

### ¿Por qué MongoDB antes que la transformación con pandas?

MongoDB guarda el JSON crudo de la API tal cual llega, antes de cualquier limpieza o transformación. Si Open-Meteo cambia un campo de su respuesta, o si una limpieza con pandas descarta una fila por error, el dato crudo original sigue disponible en MongoDB para reprocesar.

### ¿Por qué separar el código en módulos (`extract`, `raw_store`, `transform`, `load`)?

Cada módulo puede fallar y probarse de forma aislada. Si la limpieza de datos rompe algo, queda claro que el problema está en `transform.py` y no en la extracción, el guardado en Mongo o la carga a SQL Server.

## Estructura del proyecto planeada

```
weather-insight/
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── src/
│   └── weather_insight/
│       ├── __init__.py
│       ├── config.py
│       ├── extract.py
│       ├── raw_store.py
│       ├── transform.py
│       ├── load.py
│       ├── pipeline.py
│       └── logging_config.py
├── tests/
└── notebooks/
```

## Puesta en marcha

```bash
git clone git@github.com:usuario/weather-insight.git
cd weather-insight

python -m venv .venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
cp .env.example .env         # completar con la configuración local

docker compose up -d
```

## Preguntas que se planea que responda el dashboard

- ¿Va a llover hoy?
- ¿Lloverá en la semana?
- ¿Cuándo fue el último día que llovió?
- ¿Cuál fue la temperatura máxima esta semana?
- ¿Qué porcentaje de humedad suele haber a determinada hora?
- ¿Qué tan precisa fue la predicción del día anterior?

## Estado actual

- [x] Fase 1 — Extracción desde Open-Meteo con manejo de errores de red
- [ ] Fase 2 — Capa de datos crudos en MongoDB
- [ ] Fase 3 — Transformación con pandas (sobre los datos ya guardados en Mongo)
- [ ] Fase 4 — Carga a SQL Server
- [ ] Fase 5 — Automatización con Docker + cron
- [ ] Fase 6 — Dashboards en Power BI
- [ ] Fase 7 — Mejoras (alertas, comparación pronóstico vs. realidad, tests, logging)
