# Panel web Arduino JSON

Aplicación web minimalista y profesional para mostrar datos de sensores recibidos por Python en formato JSON. Mientras el Arduino no esté conectado, la API HTTP genera lecturas simuladas para validar el flujo completo.

## Características

- Vista **Dato uno a uno** con tarjetas individuales por sensor.
- Vista **Todos los datos** con una tabla de historial reciente.
- API JSON lista para reemplazar la simulación por los datos reales del Arduino.
- Actualización automática cada 2.5 segundos y botón de actualización manual.

## Ejecutar localmente

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # opcional, solo para pruebas
python app.py
```

Después abre `http://localhost:5000`.

## Endpoints disponibles

- `GET /api/status`: estado de la conexión y modo actual.
- `GET /api/reading`: una lectura simulada en formato JSON.
- `GET /api/readings`: historial de lecturas simuladas.

## Integración futura con Arduino

Cuando el Arduino envíe datos JSON desde el script de Python, reemplaza la función `get_latest_reading()` en `app.py` para que retorne el diccionario leído desde el puerto serial. Mantén las mismas claves JSON (`temperature_c`, `humidity_percent`, `light_lux`, `gas_ppm`, `distance_cm`, `motion_detected`, `timestamp`) para que la página no requiera cambios.
