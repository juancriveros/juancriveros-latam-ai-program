# Week 3 Lab: Intro to Model Context Protocol (MCP)

Level: Foundation → Applied | Est. Time: 60–90 min core / +60 stretch | Prereq: Week 2 RAG lab complete

---
## 1. Objectives
By the end you can:
1. Define the Model Context Protocol (MCP) and why tool standardization matters
2. Wrap a simple REST API as an MCP tool (weather or mock Jira)
3. Register the tool within an agent runtime (Agnos AI placeholder) and invoke via natural language
4. Trace a tool-enabled interaction (intent → tool call → response)
5. Log & evaluate tool invocation correctness vs hallucinated answers

---
## 2. What is MCP?
Model Context Protocol is an emerging standard that defines how Large Language Models (or agent runtimes acting on their behalf) discover, describe, and invoke tools consistently. It provides:
- A schema for declaring tools (capabilities, parameters, return types)
- A mechanism for runtime negotiation (what tools are available?)
- A consistent contract enabling portability across providers

Why it matters now:
| Problem Without MCP | Impact | MCP Benefit |
|---------------------|--------|------------|
| Ad-hoc tool wrappers | Inconsistent interfaces | Standard descriptors |
| Fragile prompt-based tool calling | Hallucinated invocations | Structured capability negotiation |
| Vendor lock-in | Rewrites per platform | Portable abstraction |
| Limited introspection | Poor debugging | Declarative metadata |

---
## 3. Quick Start (TL;DR)
```bash
# 1. Activate environment (reuse .venv from prior weeks)
source .venv/bin/activate

# 2. Install any new deps (placeholder if needed)
# pip install fastapi uvicorn requests pydantic

# 3. Run mock weather API (if you build one)
python w3_mcp_intro/mcp_weather_tool.py --serve-api &

# 4. Launch agent runner (registers tool schema)
python w3_mcp_intro/mcp_agent_runner.py --query "What is the weather in Madrid?"

# 5. Inspect logged tool call + model answer
```

---
## 4. Architecture (Minimal)
```
User Prompt → Agent Parser → Intent: weather.query(city)
         ↓                     ↓
     MCP Tool Registry ----> Capability Descriptor (JSON)
         ↓
  Tool Invocation (HTTP GET /weather?city=...) → Response JSON
         ↓
  Augment Model Context → LLM → Grounded Answer (with source)
```
Improvement Axes: tool schema richness, input validation, error handling, caching, parallel tool calls.

---
## 5. Core Tasks
| # | Task | Description | Acceptance |
|---|------|-------------|------------|
| 1 | Baseline Tool Schema | Define JSON schema for `get_weather(city)` | Schema file or Python dict logged |
| 2 | Mock API | Return deterministic JSON for `city` | `curl localhost:PORT/weather?city=Paris` works |
| 3 | Tool Wrapper | Expose function abiding by MCP schema | Wrapper prints structured request/response |
| 4 | Registration | Add tool to registry consumed by agent | Registry listing shows `get_weather` |
| 5 | Invocation | Natural language triggers tool call | Logs show intent → tool exec → answer |
| 6 | No-Tool Control | Compare answer w/out tool context | Difference recorded in Playbook |
| 7 | Error Path | Simulate city not found → graceful reply | Returns helpful error message |

---
## 6. Suggested Implementation Order
1. Hardcode tool metadata (name, description, params)
2. Build a simple FastAPI (or Flask) endpoint OR fully in-process stub
3. Write wrapper: parse user NL → detect need for weather (keyword or regex) → call tool
4. Generate answer template including tool JSON
5. Add fallback: if parsing fails, respond “Need city name.”
6. Add evaluation logging (tool_used, latency_ms, success_bool)

---
## 7. Evaluation & Logging
Log rows in `PROMPT_PLAYBOOK.md` (Week 3 section):
| Query | Intent Parsed | Tool? | Tool Latency ms | Success | Answer Quality (1–5) | Notes |
|-------|---------------|-------|-----------------|---------|----------------------|-------|

Success Criteria:
- Tool invoked only when needed
- City parameter extracted correctly (≥3 test cities)
- Error handled (unknown city) without crash
- Answer cites tool data explicitly (e.g., “According to tool…”) 

---
## 8. Failure Modes
| Mode | Description | Mitigation |
|------|-------------|------------|
| False Positive | Tool called when no weather intent | Better intent classifier / threshold |
| False Negative | Missed weather query | Expand pattern list / few-shot examples |
| Hallucinated Data | Answer fabricates temps | Enforce explicit citation from result JSON |
| Stale Response | Cached outdated value | Cache invalidation timeout |
| Tool Error Leak | Raw traceback in answer | Wrap exceptions, return friendly message |

---
## 9. Stretch Goals
| Category | Idea | Hint |
|----------|------|------|
| Multi-Tool | Add `time` or `currency` tool | Separate capability descriptors |
| Parallel | Run 2 tools then aggregate | Async gather (asyncio) |
| Validation | Pydantic schema on responses | Enforce required fields |
| Auth | API key requirement | Inject header from env var |
| Caching | Memoize weather by (city, minute) | Dict with TTL |
| Observability | Add structured tracing spans | Use `time.time()` & IDs |

---
## 10. Deliverables
Minimum:
1. `mcp_weather_tool.py` (tool schema + mock API OR in-process stub)
2. `mcp_agent_runner.py` (basic NL intent → tool call integration)
3. Week 3 section in `PROMPT_PLAYBOOK.md` with ≥5 logged queries

Stretch: multi-tool extension + latency metrics + error simulation.

Commit Message Guideline: `week3: add mcp weather tool baseline`

---
## 11. Reflection Prompts
- When did the tool invocation NOT improve answer quality?
- Which failure mode appeared first? Root cause?
- Next production hardening step you’d prioritize?

---
## 12. Next Week Preview
You will design user-centric agent experience (AX): structured responses, error flows, and feedback loops.

---
## Appendix: Minimal Tool Descriptor (Example)
```python
tool_descriptor = {
  "name": "get_weather",
  "description": "Return current weather for a given city (mock).",
  "inputs": [{"name": "city", "type": "string", "required": True}],
  "outputs": {"type": "object", "properties": {"city": {"type": "string"}, "temp_c": {"type": "number"}, "conditions": {"type": "string"}}}
}
```

*End of Week 3 Lab Instructions*
