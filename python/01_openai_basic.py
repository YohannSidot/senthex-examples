"""Minimal Senthex integration: swap base_url, add X-Senthex-Key, done.

Reads the verdict from response headers without changing how you call OpenAI.
Run: python 01_openai_basic.py
"""

import os

from openai import OpenAI

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
    base_url="https://app.senthex.com/v1",
    default_headers={"X-Senthex-Key": os.environ["SENTHEX_API_KEY"]},
)

raw = client.chat.completions.with_raw_response.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Say hi in one short sentence."}],
)

print(f"Request-Id:      {raw.headers.get('X-Senthex-Request-Id')}")
print(f"Shield-Status:   {raw.headers.get('X-Senthex-Shield-Status')}")
print(f"Injection-Score: {raw.headers.get('X-Senthex-Injection-Score')}")
print(f"Latency-Ms:      {raw.headers.get('X-Senthex-Latency-Ms')}")
print()

response = raw.parse()
print(response.choices[0].message.content)
