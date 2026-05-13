"""Senthex passes SSE through transparently.

The shield verdict is in the response headers, emitted *before* the first
SSE chunk — so you can inspect Shield-Status before any tokens stream.
Run: python 02_openai_streaming.py
"""

import os
import sys

from openai import OpenAI

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
    base_url="https://app.senthex.com/v1",
    default_headers={"X-Senthex-Key": os.environ["SENTHEX_API_KEY"]},
)

raw = client.chat.completions.with_raw_response.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Count from 1 to 5, one number per line."}],
    stream=True,
)

print(f"Request-Id:      {raw.headers.get('X-Senthex-Request-Id')}")
print(f"Shield-Status:   {raw.headers.get('X-Senthex-Shield-Status')}")
print(f"Injection-Score: {raw.headers.get('X-Senthex-Injection-Score')}")
print("---")

stream = raw.parse()
for chunk in stream:
    if not chunk.choices:
        continue
    delta = chunk.choices[0].delta.content
    if delta:
        sys.stdout.write(delta)
        sys.stdout.flush()
print()
