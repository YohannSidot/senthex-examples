/**
 * Same pattern, Anthropic SDK on /v1/messages.
 * Run: npx tsx 02-anthropic-basic.ts
 */
import Anthropic from "@anthropic-ai/sdk";

const anthropicKey = process.env.ANTHROPIC_API_KEY;
const senthexKey = process.env.SENTHEX_API_KEY;
if (!anthropicKey || !senthexKey) {
  throw new Error("ANTHROPIC_API_KEY and SENTHEX_API_KEY must both be set");
}

const client = new Anthropic({
  apiKey: anthropicKey,
  baseURL: "https://app.senthex.com",
  defaultHeaders: { "X-Senthex-Key": senthexKey },
});

const { data, response } = await client.messages
  .create({
    model: "claude-3-5-haiku-20241022",
    max_tokens: 256,
    messages: [{ role: "user", content: "Say hi in one short sentence." }],
  })
  .withResponse();

console.log(`Request-Id:      ${response.headers.get("x-senthex-request-id")}`);
console.log(`Shield-Status:   ${response.headers.get("x-senthex-shield-status")}`);
console.log(`Injection-Score: ${response.headers.get("x-senthex-injection-score")}`);
console.log(`Latency-Ms:      ${response.headers.get("x-senthex-latency-ms")}`);
console.log();

const block = data.content[0];
if (block && block.type === "text") {
  console.log(block.text);
}
