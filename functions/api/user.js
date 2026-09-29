// Cloudflare Pages Function: /api/user
// Automatically extracts the Google user email from Cloudflare Access headers

export async function onRequestGet(context) {
  const { request, env } = context;
  
  // Extract Cloudflare Access Authenticated Email
  const cfEmail = request.headers.get("cf-access-authenticated-user-email");
  
  return new Response(JSON.stringify({
    authenticated: !!cfEmail,
    email: cfEmail ? cfEmail.toLowerCase().trim() : null,
    adminEmail: "happyclone96@gmail.com",
    isAdmin: cfEmail && cfEmail.toLowerCase().trim() === "happyclone96@gmail.com"
  }), {
    headers: {
      "Content-Type": "application/json",
      "Cache-Control": "no-store"
    }
  });
}
