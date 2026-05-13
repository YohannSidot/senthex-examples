# Python examples

Six self-contained scripts (each < 80 lines). All use the **official provider SDK** with `base_url="https://app.senthex.com/v1"` — no Senthex Python package, no monkey-patching, no LangChain plugin.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# From the repo root: cp .env.example .env, fill values, then export:
set -a; source ../.env; set +a
```

Requires Python 3.10+.

## Examples

| File | What it shows |
|------|---------------|
| `01_openai_basic.py` | Minimal swap: `base_url` + `X-Senthex-Key`, print 4 verdict headers. |
| `02_openai_streaming.py` | SSE streaming — headers arrive before the first token. |
| `03_anthropic_basic.py` | Same pattern via the Anthropic SDK (`/v1/messages`). |
| `04_prompt_injection_demo.py` | Three real attacks — see the shields actually fire. |
| `05_per_agent_tracking.py` | Per-agent trust isolation via `X-Senthex-Agent-Id` / `-Session-Id`. |
| `06_langchain_integration.py` | `langchain-openai` over Senthex with zero extra dependencies. |

## Run them

```bash
python 01_openai_basic.py
python 04_prompt_injection_demo.py    # show this one to your team
```

## How to read Senthex response headers

The default `client.chat.completions.create(...)` discards the raw HTTP response. Senthex headers (`X-Senthex-Shield-Status`, `-Injection-Score`, etc.) only surface when you opt in:

```python
raw = client.chat.completions.with_raw_response.create(...)
print(raw.headers.get("X-Senthex-Shield-Status"))
response = raw.parse()           # → ChatCompletion
```

For Anthropic, the same idea: `client.messages.with_raw_response.create(...)` exposes `.headers` and `.parse()`.

To send extra request headers (per-call agent / session IDs), use the SDK's `extra_headers=` argument on `create(...)` instead of rebuilding the client.

## Notes

- Senthex never stores your provider key. `Authorization` (OpenAI/Mistral) or `x-api-key` (Anthropic) is forwarded verbatim to the upstream API.
- The proxy adds < 50 ms of overhead; the actual value is exposed in `X-Senthex-Latency-Ms`.
- Streaming: all `X-Senthex-*` headers are emitted **before the first SSE chunk**, so you can decide to abort early on `Shield-Status: warn`.
