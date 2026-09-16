const PROMPTS_HOST = "prompts.robertdevore.com";
const RETIRED_PROMPT = "/blog/wwf-action-figure-blister-pack-json-prompt";

export default {
	async fetch(request) {
		const url = new URL(request.url);

		if (url.hostname === "wwf.robertdevore.com") {
			return Response.redirect("https://robertdevore.com/", 301);
		}

		if (
			url.hostname === PROMPTS_HOST &&
			(url.pathname === RETIRED_PROMPT ||
				url.pathname === RETIRED_PROMPT + "/" ||
				url.pathname === RETIRED_PROMPT + ".html")
		) {
			return Response.redirect("https://prompts.robertdevore.com/", 301);
		}

		return fetch(request);
	},
};
