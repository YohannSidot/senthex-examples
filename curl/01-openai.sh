#!/usr/bin/env bash
# Minimal Senthex integration via curl — no SDK, no dependencies.
# Required env: SENTHEX_API_KEY, OPENAI_API_KEY.
# Optional: pretty-prints JSON via jq if installed.
# Run: bash 01-openai.sh
set -euo pipefail

: "${SENTHEX_API_KEY:?SENTHEX_API_KEY must be set}"
: "${OPENAI_API_KEY:?OPENAI_API_KEY must be set}"

tmpdir=$(mktemp -d)
trap 'rm -rf "$tmpdir"' EXIT
headers="$tmpdir/headers"
body="$tmpdir/body"

curl -sS https://app.senthex.com/v1/chat/completions \
  -D "$headers" \
  -o "$body" \
  -H "Authorization: Bearer ${OPENAI_API_KEY}" \
  -H "X-Senthex-Key: ${SENTHEX_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [{"role": "user", "content": "Say hi in one short sentence."}]
  }'

echo "# Senthex response headers"
grep -i '^x-senthex-' "$headers" | sort

echo
echo "# Response body"
if command -v jq >/dev/null 2>&1; then
  jq -r '.choices[0].message.content' "$body"
else
  cat "$body"
fi
