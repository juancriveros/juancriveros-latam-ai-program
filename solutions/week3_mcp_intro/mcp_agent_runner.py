"""Minimal agent runner that simulates MCP-style tool registration and invocation.

Flow:
1. Load tool descriptor (import from mcp_weather_tool)
2. Parse user natural language query for weather intent (regex/keywords)
3. If intent detected: extract city, invoke tool (function or HTTP)
4. Construct answer citing tool data (avoid hallucination)
5. Log structured record (JSON) for Playbook usage

NOTE: This is an instructional scaffold, not a production MCP client.
"""
from __future__ import annotations
import argparse
import json
import re
import time
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any

try:
    from mcp_weather_tool import invoke_get_weather, TOOL_DESCRIPTOR  # type: ignore
except ImportError:  # pragma: no cover
    raise SystemExit("Run from project root so Python can resolve mcp_weather_tool.")

WEATHER_PATTERN = re.compile(r"weather (?:in|at|for) (?P<city>[A-Za-z\-\s]+)\??", re.IGNORECASE)

@dataclass
class InvocationLog:
    query: str
    intent: Optional[str]
    tool_used: bool
    params: Dict[str, Any]
    success: bool
    latency_ms: float
    error: Optional[str]
    answer: str


def parse_intent(query: str) -> Optional[str]:
    if WEATHER_PATTERN.search(query):
        return "get_weather"
    return None


def extract_city(query: str) -> Optional[str]:
    m = WEATHER_PATTERN.search(query)
    return m.group("city").strip() if m else None


def answer_without_tool(query: str) -> str:
    return (
        "I can provide weather if you phrase it like 'weather in <city>'. "
        "Try again specifying a city."
    )


def build_answer_with_tool(query: str, weather: Dict[str, Any]) -> str:
    return (
        f"Weather for {weather['city']}: {weather['temp_c']}°C, {weather['conditions']}. "
        f"(Source: {weather['source']})."
    )


def run_agent(query: str) -> InvocationLog:
    intent = parse_intent(query)
    if intent != "get_weather":
        ans = answer_without_tool(query)
        return InvocationLog(query, intent, False, {}, True, 0.0, None, ans)

    city = extract_city(query)
    start = time.time()
    params: Dict[str, Any] = {"city": city}
    try:
        if not city:
            raise ValueError("City not detected. Use format 'weather in <city>'.")
        weather = invoke_get_weather(city)
        ans = build_answer_with_tool(query, weather)
        latency = (time.time() - start) * 1000
        return InvocationLog(query, intent, True, params, True, latency, None, ans)
    except Exception as e:  # pylint: disable=broad-except
        latency = (time.time() - start) * 1000
        return InvocationLog(query, intent, True, params, False, latency, str(e), f"Error: {e}")


def main():
    parser = argparse.ArgumentParser(description="Minimal MCP-style agent runner")
    parser.add_argument("--query", type=str, required=True, help="User natural language query")
    parser.add_argument("--log-json", type=str, help="Optional path to append JSON log line")
    args = parser.parse_args()

    log = run_agent(args.query)
    print("Answer:\n" + log.answer)
    print("\nInvocation Log:")
    print(json.dumps(asdict(log), indent=2))

    if args.log_json:
        with open(args.log_json, "a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(log)) + "\n")
            print(f"Appended log to {args.log_json}")


if __name__ == "__main__":  # pragma: no cover
    main()
