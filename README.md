# Secure every LLM call. Change one line of code.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Made in France](https://img.shields.io/badge/Made%20in-France%20%F0%9F%87%AB%F0%9F%87%B7-002654)](https://senthex.com)
[![EU AI Act Ready](https://img.shields.io/badge/EU%20AI%20Act-Ready-00C48C)](https://senthex.com)

Most LLM security tools sit at the orchestration layer — they need an SDK, an agent framework, or a sidecar. Senthex sits at the LLM API boundary. Every call from your app to OpenAI, Anthropic, Mistral, Google or OpenRouter runs through 28 shields (prompt injection, PII, jailbreaks, intent classification, anomaly detection, multi-turn attacks, semantic hijack, toxicity, …), and you get a full audit trail in HTTP response headers — EU-hosted, RGPD by design.

This repo shows you how to enable it. No new SDK. No vendor lock-in. Just swap `base_url`.

## The diff

```python
from openai import OpenAI

# Before — direct to OpenAI
client = OpenAI(
    api_key="sk-...",
)

# After — three lines route every call through Senthex
client = OpenAI(
    api_key="sk-...",
    base_url="https://app.senthex.com/v1",
    default_headers={"X-Senthex-Key": "snx-..."},
)
```

That's it. Your existing `client.chat.completions.create(...)` code keeps working. The same pattern applies to `anthropic`, `mistralai`, `langchain-openai`, and raw `curl`.

## Quickstart

1. **Sign up** at [senthex.com](https://senthex.com) — Free tier, 1000 requests/month, no credit card.
2. **Copy your key** from the dashboard. It starts with `snx-`.
3. **Run an example:**
   ```bash
   git clone https://github.com/senthex/senthex-examples.git
   cd senthex-examples
   cp .env.example .env   # fill SENTHEX_API_KEY and OPENAI_API_KEY
   pip install -r python/requirements.txt
   set -a; source .env; set +a
   python python/01_openai_basic.py
   ```

## What you see — `X-Senthex-*` response headers

Every response carries a forensic trail in HTTP headers. The 5 you'll inspect most:

| Header | Type | Meaning |
|--------|------|---------|
| `X-Senthex-Request-Id` | uuid | Correlate with your dashboard / logs |
| `X-Senthex-Shield-Status` | `pass` \| `warn` \| `block` | Verdict for this call |
| `X-Senthex-Injection-Score` | float `0.0`–`1.0` | Prompt injection confidence |
| `X-Senthex-PII-Found` | int | Number of PII entities detected in the request |
| `X-Senthex-Latency-Ms` | float | Shield overhead (sub-50 ms target) |

Plus ~25 more (`X-Senthex-Intent-Risk`, `X-Senthex-Trust-Level`, `X-Senthex-Data-Classification`, `X-Senthex-Toxicity-Score`, `X-Senthex-Anomaly-Score`, `X-Senthex-Semantic-Hijack`, `X-Senthex-Session-Injection-Score`, …) — see the Python examples for direct access via `with_raw_response`.

A clean call from `curl/01-openai.sh`:

```
HTTP/2 200
x-senthex-request-id: 8b3e4a17-2f6c-4d99-9c0d-1e7c4a2b8d31
x-senthex-shield-status: pass
x-senthex-injection-score: 0.12
x-senthex-pii-found: 0
x-senthex-intent-risk: none
x-senthex-trust-level: normal
x-senthex-data-classification: PUBLIC
x-senthex-latency-ms: 38.42
```

## Languages

- **[Python](python/)** — 6 examples covering OpenAI, Anthropic, streaming, prompt-injection detection, per-agent tracking, LangChain.
- **[TypeScript](typescript/)** — OpenAI + Anthropic with the official SDKs in strict mode.
- **[curl](curl/)** — pure HTTP, no SDK, for shell scripts and CI smoke tests.

## What's in the box

| File | What it shows |
|------|---------------|
| [`python/01_openai_basic.py`](python/01_openai_basic.py) | Minimal `base_url` swap + read 3 Senthex headers |
| [`python/02_openai_streaming.py`](python/02_openai_streaming.py) | SSE streaming with header inspection before the first token |
| [`python/03_anthropic_basic.py`](python/03_anthropic_basic.py) | Same pattern for the Anthropic SDK (`/v1/messages`) |
| [`python/04_prompt_injection_demo.py`](python/04_prompt_injection_demo.py) | Three real attacks (instruction override, DAN, credit-card PII) and what Senthex does with each |
| [`python/05_per_agent_tracking.py`](python/05_per_agent_tracking.py) | `X-Senthex-Agent-Id` + `X-Senthex-Session-Id` — trust degrades per-agent, not globally |
| [`python/06_langchain_integration.py`](python/06_langchain_integration.py) | `ChatOpenAI(base_url=..., default_headers=...)` — no Senthex SDK required |

## Pricing & limits

Free 1k req/month → Pro €49 (100k) → Business €199 (1M) → Enterprise from €999. See [senthex.com/pricing](https://senthex.com/pricing).

## Try the Free tier at [senthex.com](https://senthex.com)

No credit card, no trial expiry, no commit. If you ship LLM features in production, ten minutes here is worth it.

---

Made in France 🇫🇷 · MIT licensed · Issues and PRs welcome at [github.com/senthex/senthex-examples/issues](https://github.com/senthex/senthex-examples/issues)
