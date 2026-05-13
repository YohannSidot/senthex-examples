#!/usr/bin/env bash
# SSE streaming through Senthex. The proxy sets X-Senthex-* headers BEFORE
# the first SSE chunk arrives, so we capture them with -D and stream the
# body to stdout unbuffered.
#
# OpenAI SSE format: lines of `data: {...}\n\n`, terminated by `data: [DONE]`.
#
# Required env: SENTHEX_API_KEY, OPENAI_API_KEY.
# Run: bash 02-streaming.sh
set -euo pipefail

: "${SENTHEX_API_KEY:?SENTHEX_API_KEY must be set}"
: "${OPENAI_API_KEY:?OPENAI_API_KEY must be set}"

headers=$(mktemp)
trap 'rm -f "$headers"' EXIT

echo "# Streaming response (tokens incoming)"
echo "---"

curl -sSN https://app.senthex.com/v1/chat/completions \
  --no-buffer \
  -D "$headers" \
  -H "Authorization: Bearer ${OPENAI_API_KEY}" \
  -H "X-Senthex-Key: ${SENTHEX_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [{"role": "user", "content": "Count from 1 to 5, one number per line."}],
    "stream": true
  }'

echo
echo "---"
echo "# Senthex headers (emitted before the first chunk)"
grep -i '^x-senthex-' "$headers" | sort
