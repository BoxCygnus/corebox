// Cloudflare Pages Advanced Worker: Handles /api routes with Cloudflare KV storage
// All other requests are passed to static assets (env.ASSETS)

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // 1. API: /api/users
    if (url.pathname === "/api/users") {
      const headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
        "Cache-Control": "no-store, no-cache, must-revalidate",
      };

      if (request.method === "OPTIONS") {
        return new Response(null, { headers });
      }

      const defaultAdmin = {
        "happyclone96@gmail.com": {
          email: "happyclone96@gmail.com",
          full_name: "System Administrator",
          role: "admin",
          status: "active",
          created_at: new Date().toISOString().replace("T", " ").substring(0, 19),
          updated_at: new Date().toISOString().replace("T", " ").substring(0, 19)
        }
      };

      let usersStore = defaultAdmin;
      if (env.COREBOX_STORAGE) {
        try {
          const raw = await env.COREBOX_STORAGE.get("corebox_users_store");
          if (raw) {
            usersStore = JSON.parse(raw);
          }
        } catch (e) {
          console.error("KV read users error:", e);
        }
      }

      // Always ensure admin exists
      if (!usersStore["happyclone96@gmail.com"]) {
        usersStore["happyclone96@gmail.com"] = defaultAdmin["happyclone96@gmail.com"];
      }

      if (request.method === "GET") {
        return new Response(JSON.stringify({ success: true, users: usersStore }), { headers });
      }

      if (request.method === "POST") {
        try {
          const body = await request.json();
          const nowStr = new Date().toISOString().replace("T", " ").substring(0, 19);

          if (body.action === "update_status" && body.email) {
            const e = body.email.toLowerCase().trim();
            if (usersStore[e]) {
              usersStore[e].status = body.status;
              usersStore[e].updated_at = nowStr;
            }
          } else if (body.action === "delete" && body.email) {
            const e = body.email.toLowerCase().trim();
            if (e !== "happyclone96@gmail.com") {
              delete usersStore[e];
            }
          } else if (body.users && typeof body.users === "object") {
            // Bulk replace or merge
            usersStore = Object.assign({}, usersStore, body.users);
          } else if (body.email) {
            // Single user register / upsert
            const e = body.email.toLowerCase().trim();
            const isAdmin = (e === "happyclone96@gmail.com");
            if (!usersStore[e]) {
              usersStore[e] = {
                email: e,
                full_name: body.full_name || e.split("@")[0],
                role: isAdmin ? "admin" : (body.role || "user"),
                status: isAdmin ? "active" : (body.status || "pending"),
                created_at: nowStr,
                updated_at: nowStr
              };
            } else {
              if (body.full_name) usersStore[e].full_name = body.full_name;
              if (body.status) usersStore[e].status = body.status;
              if (body.role && !isAdmin) usersStore[e].role = body.role;
              usersStore[e].updated_at = nowStr;
            }
          }

          if (env.COREBOX_STORAGE) {
            await env.COREBOX_STORAGE.put("corebox_users_store", JSON.stringify(usersStore));
          }

          return new Response(JSON.stringify({ success: true, users: usersStore }), { headers });
        } catch (err) {
          return new Response(JSON.stringify({ success: false, error: err.message }), { status: 400, headers });
        }
      }
    }

    // 2. API: /api/catalog
    if (url.pathname === "/api/catalog") {
      const headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
        "Cache-Control": "no-store, no-cache, must-revalidate",
      };

      if (request.method === "OPTIONS") {
        return new Response(null, { headers });
      }

      if (request.method === "GET") {
        let catalog = null;
        if (env.COREBOX_STORAGE) {
          try {
            const raw = await env.COREBOX_STORAGE.get("corebox_catalog_store");
            if (raw) {
              catalog = JSON.parse(raw);
            }
          } catch (e) {
            console.error("KV read catalog error:", e);
          }
        }
        return new Response(JSON.stringify({ success: true, catalog }), { headers });
      }

      if (request.method === "POST") {
        try {
          const body = await request.json();
          if (env.COREBOX_STORAGE) {
            await env.COREBOX_STORAGE.put("corebox_catalog_store", JSON.stringify(body));
          }
          return new Response(JSON.stringify({ success: true }), { headers });
        } catch (err) {
          return new Response(JSON.stringify({ success: false, error: err.message }), { status: 400, headers });
        }
      }
    }

    // Fallback: serve static assets with Cloudflare edge caching
    const res = await env.ASSETS.fetch(request);
    const newHeaders = new Headers(res.headers);
    if (url.pathname === "/" || url.pathname.endsWith(".html")) {
      newHeaders.set("Cache-Control", "public, max-age=0, must-revalidate");
    } else if (/\.(js|css|woff2|woff|ttf|png|jpg|jpeg|svg|webp|wasm|whl|json)$/i.test(url.pathname)) {
      newHeaders.set("Cache-Control", "public, max-age=31536000, immutable");
    }
    return new Response(res.body, {
      status: res.status,
      statusText: res.statusText,
      headers: newHeaders,
    });
  }
};
