"""Minimal MCP-style weather tool (mock) for Week 3 lab.

Features:
- Optionally serves a simple HTTP endpoint (stub) OR runs in-process.
- Exposes a tool descriptor (schema-like) consumable by an agent runtime.
- Provides a function `invoke_get_weather(city: str)` returning deterministic weather JSON.

NOTE: This is a simplified stand-in illustrating *concepts* of MCP. Replace with actual MCP library integration if/when adopted.
"""
from __future__ import annotations
import argparse
import json
import random
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Dict, Any

TOOL_DESCRIPTOR: Dict[str, Any] = {
    "name": "get_weather",
    "description": "Return current (mock) weather conditions for a given city.",
    "inputs": [
        {"name": "city", "type": "string", "required": True, "description": "City name (ASCII)"}
    ],
    "outputs": {
        "type": "object",
        "properties": {
            "city": {"type": "string"},
            "temp_c": {"type": "number"},
            "conditions": {"type": "string"},
            "source": {"type": "string"},
            "timestamp": {"type": "integer"}
        },
        "required": ["city", "temp_c", "conditions", "timestamp"]
    }
}

CONDITIONS = ["Sunny", "Cloudy", "Rain", "Storm", "Windy", "Partly Cloudy"]

# Deterministic-ish mapping for repeat runs (seeded by city hash)
def invoke_get_weather(city: str) -> Dict[str, Any]:
    if not city or not city.strip():
        raise ValueError("city parameter required")
    seed = abs(hash(city)) % (10 ** 6)
    rng = random.Random(seed)
    temp = round(rng.uniform(5, 32), 1)
    cond = CONDITIONS[seed % len(CONDITIONS)]
    return {
        "city": city,
        "temp_c": temp,
        "conditions": cond,
        "source": "mock-weather-service",
        "timestamp": int(time.time())
    }

class WeatherHandler(BaseHTTPRequestHandler):
    def do_GET(self):  # noqa: N802
        if self.path.startswith("/weather"):
            # naive query parsing: /weather?city=Paris
            try:
                query = self.path.split("?", 1)[1] if "?" in self.path else ""
                params = dict(p.split("=", 1) for p in query.split("&") if p)
                city = params.get("city")
                data = invoke_get_weather(city)
                self._send_json(200, data)
            except Exception as e:  # pylint: disable=broad-except
                self._send_json(400, {"error": str(e)})
        elif self.path == "/descriptor":
            self._send_json(200, TOOL_DESCRIPTOR)
        else:
            self._send_json(404, {"error": "Not Found"})

    def log_message(self, fmt, *args):  # noqa: D401
        return  # silence default logging

    def _send_json(self, code: int, payload: Dict[str, Any]):
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def serve(port: int):
    server = HTTPServer(("0.0.0.0", port), WeatherHandler)
    print(f"[mcp-weather] Serving on :{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Stopping server...")


def main():
    parser = argparse.ArgumentParser(description="Mock MCP weather tool")
    parser.add_argument("--serve-api", action="store_true", help="Run simple HTTP server")
    parser.add_argument("--port", type=int, default=8765, help="Port for HTTP server")
    parser.add_argument("--city", type=str, help="Direct invocation mode – city name")
    args = parser.parse_args()

    if args.serve_api:
        serve(args.port)
        return

    if args.city:
        try:
            result = invoke_get_weather(args.city)
            print(json.dumps(result, indent=2))
        except Exception as e:  # pylint: disable=broad-except
            print(json.dumps({"error": str(e)}))
    else:
        print(json.dumps({"descriptor": TOOL_DESCRIPTOR}, indent=2))


if __name__ == "__main__":  # pragma: no cover
    main()
