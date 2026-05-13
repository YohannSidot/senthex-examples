/**
 * Minimal Senthex integration: swap baseURL, add X-Senthex-Key, done.
 * Run: npx tsx 01-openai-basic.ts
 */
import OpenAI from "openai";

const openaiKey = process.env.OPENAI_API_KEY;
const senthexKey = process.env.SENTHEX_API_KEY;
if (!openaiKey || !senthexKey) {
  throw new Error("OPENAI_API_KEY and SENTHEX_API_KEY must both be set");
}

const client = new OpenAI({
  apiKey: openaiKey,
  baseURL: "https://app.senthex.com/v1",
  defaultHeaders: { "X-Senthex-Key": senthexKey },
});

const { data, response } = await client.chat.completions
  .create({
    model: "gpt-4o-mini",
    messages: [{ role: "user", content: "Say hi in one short sentence." }],
  })
  .withResponse();

console.log(`Request-Id:      ${response.headers.get("x-senthex-request-id")}`);
console.log(`Shield-Status:   ${response.headers.get("x-senthex-shield-status")}`);
console.log(`Injection-Score: ${response.headers.get("x-senthex-injection-score")}`);
console.log(`Latency-Ms:      ${response.headers.get("x-senthex-latency-ms")}`);
console.log();
console.log(data.choices[0]?.message.content ?? "");
