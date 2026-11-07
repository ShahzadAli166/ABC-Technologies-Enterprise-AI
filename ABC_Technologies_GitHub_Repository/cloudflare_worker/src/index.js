export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    const headers = {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Headers": "Content-Type, X-API-Key",
      "Access-Control-Allow-Methods": "GET, POST, OPTIONS"
    };

    if (request.method === "OPTIONS") {
      return new Response(null, { headers });
    }

    if (url.pathname === "/health" && request.method === "GET") {
      return Response.json({
        application: "ABC Technologies",
        gateway: "Cloudflare Workers",
        status: "healthy"
      }, { headers });
    }

    if (url.pathname !== "/api/assistant" ||
        request.method !== "POST") {
      return Response.json(
        { error: "Not found" },
        { status: 404, headers }
      );
    }

    if (!env.APP_API_KEY ||
        request.headers.get("X-API-Key") !== env.APP_API_KEY) {
      return Response.json(
        { error: "Unauthorized" },
        { status: 401, headers }
      );
    }

    if (!env.UPSTREAM_API_URL || !env.UPSTREAM_API_KEY) {
      return Response.json(
        { error: "AI upstream not connected yet" },
        { status: 503, headers }
      );
    }

    try {
      const upstream = await fetch(
        env.UPSTREAM_API_URL + "/api/assistant",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-API-Key": env.UPSTREAM_API_KEY
          },
          body: await request.text()
        }
      );

      return new Response(upstream.body, {
        status: upstream.status,
        headers
      });

    } catch (error) {
      return Response.json(
        { error: "Upstream service unavailable" },
        { status: 502, headers }
      );
    }
  }
};
