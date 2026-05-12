"""Web dashboard for simulated Arduino JSON telemetry.

The application exposes a small standard-library HTTP API that can be connected
later to the Python scripts reading Arduino serial JSON. For now it generates
realistic simulated measurements and keeps a rolling in-memory history for the
UI.
"""

from __future__ import annotations

import json
from collections import deque
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from random import uniform
from typing import Deque
from urllib.parse import urlparse

MAX_HISTORY = 40
PORT = 5000
_history: Deque[dict[str, object]] = deque(maxlen=MAX_HISTORY)


@dataclass(frozen=True)
class SensorReading:
    """Single telemetry snapshot matching the Arduino JSON contract."""

    temperature_c: float
    humidity_percent: float
    light_lux: int
    gas_ppm: int
    distance_cm: float
    motion_detected: bool
    timestamp: str


def _build_simulated_reading() -> dict[str, object]:
    """Create a realistic but deterministic-shaped sample reading."""
    reading = SensorReading(
        temperature_c=round(uniform(20.0, 31.5), 1),
        humidity_percent=round(uniform(38.0, 73.0), 1),
        light_lux=round(uniform(120, 850)),
        gas_ppm=round(uniform(180, 520)),
        distance_cm=round(uniform(8.0, 160.0), 1),
        motion_detected=uniform(0, 1) > 0.65,
        timestamp=datetime.now(timezone.utc).isoformat(timespec="seconds"),
    )
    return asdict(reading)


def get_latest_reading() -> dict[str, object]:
    """Generate and store the latest simulated Arduino JSON reading."""
    reading = _build_simulated_reading()
    _history.appendleft(reading)
    return reading


def get_readings_history() -> list[dict[str, object]]:
    """Return the rolling telemetry history, seeding it when empty."""
    if not _history:
        get_latest_reading()
    return list(_history)


def get_status() -> dict[str, object]:
    """Expose connection metadata for the web dashboard."""
    return {
        "mode": "simulation",
        "source": "Python standard-library HTTP API",
        "arduino_connected": False,
        "message": "Simulando datos hasta conectar el Arduino por JSON.",
    }


class ArduinoDashboardHandler(SimpleHTTPRequestHandler):
    """Serve the dashboard files and JSON API endpoints."""

    def do_GET(self) -> None:  # noqa: N802 - required by SimpleHTTPRequestHandler
        path = urlparse(self.path).path
        routes = {
            "/api/reading": get_latest_reading,
            "/api/readings": get_readings_history,
            "/api/status": get_status,
        }

        if path in routes:
            self._send_json(routes[path]())
            return

        if path == "/":
            self.path = "/templates/index.html"

        super().do_GET()

    def _send_json(self, payload: object) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def run_server(port: int = PORT) -> None:
    """Start the local dashboard server."""
    server = ThreadingHTTPServer(("0.0.0.0", port), ArduinoDashboardHandler)
    print(f"Panel disponible en http://localhost:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
