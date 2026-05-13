"""Same pattern, Anthropic SDK.

The Anthropic SDK appends /v1/messages to base_url itself, so we pass just
the host root — Senthex's /v1/messages endpoint is what the SDK ends up hitting.
Run: python 03_anthropic_basic.py
"""

import os

from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ["ANTHROPIC_API_KEY"],
    base_url="https://app.senthex.com",
    default_headers={"X-Senthex-Key": os.environ["SENTHEX_API_KEY"]},
)

raw = client.messages.with_raw_response.create(
    model="claude-3-5-haiku-20241022",
    max_tokens=256,
    messages=[{"role": "user", "content": "Say hi in one short sentence."}],
)

print(f"Request-Id:      {raw.headers.get('X-Senthex-Request-Id')}")
print(f"Shield-Status:   {raw.headers.get('X-Senthex-Shield-Status')}")
print(f"Injection-Score: {raw.headers.get('X-Senthex-Injection-Score')}")
print(f"Latency-Ms:      {raw.headers.get('X-Senthex-Latency-Ms')}")
print()

message = raw.parse()
print(message.content[0].text)
