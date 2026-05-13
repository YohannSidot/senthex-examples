# curl examples

Pure HTTP, no SDK. Useful for shell scripts, CI smoke tests, and confirming that Senthex is reachable from your network.

## Setup

```bash
# From the repo root: cp .env.example .env, fill values, then:
set -a; source ../.env; set +a
```

Requires `curl` (universal) and optionally `jq` to pretty-print JSON.

## Examples

| File | What it shows |
|------|---------------|
| `01-openai.sh` | POST one chat completion; dump Senthex headers + body separately. |
| `02-streaming.sh` | SSE streaming with `--no-buffer`; headers arrive before the first chunk. |

## Run them

```bash
bash 01-openai.sh
bash 02-streaming.sh
```

## Anatomy

```bash
curl https://app.senthex.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \   # forwarded verbatim to OpenAI
  -H "X-Senthex-Key: $SENTHEX_API_KEY" \         # required, snx- format
  -H "Content-Type: application/json" \
  -d '{...}'
```

`-D <file>` dumps the response headers — every `X-Senthex-*` line shows up there. Add `-N --no-buffer` for streaming endpoints (`"stream": true`).
