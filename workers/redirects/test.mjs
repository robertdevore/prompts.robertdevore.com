import assert from "node:assert/strict";
import test from "node:test";

import worker from "./src/index.mjs";

test("redirects the retired WWF subdomain to robertdevore.com", async () => {
	const response = await worker.fetch(new Request("https://wwf.robertdevore.com/anything?old=1"));

	assert.equal(response.status, 301);
	assert.equal(response.headers.get("location"), "https://robertdevore.com/");
});

test("redirects retired prompt aliases to the prompt library home", async () => {
	for (const path of [
		"/blog/wwf-action-figure-blister-pack-json-prompt",
		"/blog/wwf-action-figure-blister-pack-json-prompt/",
		"/blog/wwf-action-figure-blister-pack-json-prompt.html",
	]) {
		const response = await worker.fetch(new Request("https://prompts.robertdevore.com" + path));
		assert.equal(response.status, 301);
		assert.equal(response.headers.get("location"), "https://prompts.robertdevore.com/");
	}
});
