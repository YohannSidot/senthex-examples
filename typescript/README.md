# TypeScript examples

Two strict-mode TS scripts, official provider SDKs only.

## Setup

```bash
npm install
# From the repo root: cp .env.example .env, fill values, then:
set -a; source ../.env; set +a
```

Requires Node 20+.

## Examples

| File | What it shows |
|------|---------------|
| `01-openai-basic.ts` | `new OpenAI({ baseURL, defaultHeaders })` + read 3 Senthex headers via `.withResponse()`. |
| `02-anthropic-basic.ts` | Same pattern for `@anthropic-ai/sdk` against `/v1/messages`. |

## Run them

```bash
npm run basic
npm run anthropic
```

## How to read Senthex headers in TypeScript

The OpenAI and Anthropic Node SDKs both expose `.withResponse()` on a returned promise:

```ts
const { data, response } = await client.chat.completions
  .create({ ... })
  .withResponse();

response.headers.get("x-senthex-shield-status");
```

`response` is a standard `Response`, so `response.headers.get(...)` returns the header value (case-insensitive).

## Notes

- Strict-mode safe: `process.env.*` is `string | undefined`, so the examples narrow it via a local-const + null check before constructing the client.
- For per-call request headers (e.g. `X-Senthex-Agent-Id`), pass them as a second arg to `create(...)` in the OpenAI SDK: `{ headers: { "X-Senthex-Agent-Id": "..." } }`.
