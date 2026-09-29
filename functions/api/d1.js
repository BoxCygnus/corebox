// Cloudflare Pages Function: /api/d1
// Handles SQL query execution on Cloudflare D1 database

export async function onRequestPost(context) {
  const { request, env } = context;
  
  if (!env.DB) {
    return new Response(JSON.stringify({
      error: "D1 database binding 'DB' is not configured in Cloudflare Pages."
    }), { status: 500, headers: { "Content-Type": "application/json" } });
  }

  try {
    const { sql, params = [] } = await request.json();
    if (!sql) {
      return new Response(JSON.stringify({ error: "Missing SQL query" }), { status: 400 });
    }

    const stmt = env.DB.prepare(sql).bind(...params);
    const result = await stmt.all();

    return new Response(JSON.stringify({
      success: true,
      results: result.results || []
    }), {
      headers: { "Content-Type": "application/json" }
    });
  } catch (err) {
    return new Response(JSON.stringify({
      error: err.message
    }), { status: 500, headers: { "Content-Type": "application/json" } });
  }
}
