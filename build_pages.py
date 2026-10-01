import os
import json

def build_pages_app():
    """
    Builds the standalone Cloudflare Pages distribution (public/index.html).
    This bundles the Python application to run directly on https://<project>.pages.dev
    using WebAssembly / Pyodide (Stlite), requiring ZERO backend servers!
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    public_dir = os.path.join(base_dir, "public")
    os.makedirs(public_dir, exist_ok=True)

    # Collect all python source files to bundle
    files_to_bundle = [
        "app.py",
        "auth.py",
        "config.py",
        "i18n.py",
        "database.py",
        "parsers.py",
        "styles.py",
        "navbar.py",
        "views/home.py",
        "views/pending.py",
        "views/users.py",
        "views/repository.py",
        "views/inspection.py",
        "views/login.py",
        "catalog_store.json",
        "users_store.json",
    ]

    bundle_dict = {}
    for rel_path in files_to_bundle:
        full_path = os.path.join(base_dir, rel_path.replace("/", os.sep))
        if os.path.exists(full_path):
            with open(full_path, "r", encoding="utf-8") as f:
                bundle_dict[rel_path.replace("\\", "/")] = f.read()
        else:
            print(f"Warning: File not found: {full_path}")

    files_json = json.dumps(bundle_dict, ensure_ascii=False).replace("<", "\\u003c")

    html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
  <title>Corebox — Đơn giản hóa công việc của bạn.</title>
  <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>📦</text></svg>">
  <link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin />
  <link rel="dns-prefetch" href="https://cdn.jsdelivr.net" />
  <link rel="preconnect" href="https://accounts.google.com" crossorigin />
  <link rel="preload" href="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.73.1/build/stlite.js" as="script" />
  <link rel="preload" href="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.73.1/build/stlite.css" as="style" />
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.73.1/build/stlite.css" />
  <script src="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.73.1/build/stlite.js"></script>
  <script src="https://accounts.google.com/gsi/client" async defer></script>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; }}
    html, body {{
      margin: 0 !important;
      padding: 0 !important;
      width: 100% !important;
      height: 100% !important;
      background-color: #0b0f19 !important;
      color: #f1f5f9 !important;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
      overflow-x: hidden !important;
    }}
    /* HIDE ALL STREAMLIT CHROME */
    header, .stAppHeader,
    [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"],
    [data-testid="stStatusWidget"], .stStatusWidget, [data-testid="stToolbarActions"],
    .Toastify__toast-container, .Toastify__toast,
    .Toastify__toast--default, .Toastify__toast--info,
    [class*="Toastify"], .stlite-message, #MainMenu, .stDeployButton,
    div:has(> [data-testid="stStatusWidget"]), div[data-testid="stStatusWidget"] * {{
      display: none !important;
      height: 0 !important;
      min-height: 0 !important;
      max-height: 0 !important;
      width: 0 !important;
      padding: 0 !important;
      margin: 0 !important;
      visibility: hidden !important;
      opacity: 0 !important;
      overflow: hidden !important;
      pointer-events: none !important;
      border: none !important;
    }}
    /* FULL FLUSH RESET: Streamlit App root containers */
    [data-testid="stApp"], .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"], section[data-testid="stMain"],
    section.main, .main {{
      margin: 0 !important;
      padding: 0 !important;
      top: 0 !important;
      left: 0 !important;
      width: 100% !important;
      max-width: 100vw !important;
      background-color: #0b0e17 !important;
      overflow-x: hidden !important;
    }}
    /* BLOCK CONTAINER: zero padding all sides */
    .main .block-container,
    [data-testid="stMainBlockContainer"],
    [data-testid="block-container"],
    div[data-testid="stAppViewBlockContainer"],
    div[class*="block-container"] {{
      padding: 0 !important;
      margin: 0 !important;
      max-width: 100vw !important;
      width: 100% !important;
      box-sizing: border-box !important;
    }}
    /* NAVBAR: full-width flush at top, padded inside */
    .corebox-navbar-container {{
      position: sticky !important;
      top: 0 !important;
      z-index: 999999 !important;
      background-color: #0b0e17 !important;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6) !important;
      padding-top: 0.45rem !important;
      padding-bottom: 0.45rem !important;
      padding-left: 1.8rem !important;
      padding-right: 1.8rem !important;
      margin: 0 !important;
      width: 100% !important;
      box-sizing: border-box !important;
    }}
    /* NAV LOGIN PILL BUTTON */
    .nav-login-btn-wrapper {{ display: inline-flex; align-items: center; }}
    .nav-login-pill-btn {{
      display: inline-flex !important;
      align-items: center !important;
      gap: 0.45rem !important;
      padding: 0.38rem 1.1rem !important;
      border-radius: 9999px !important;
      background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%) !important;
      color: #0b0f19 !important;
      font-size: 0.9rem !important;
      font-weight: 700 !important;
      text-decoration: none !important;
      border: none !important;
      outline: none !important;
      cursor: pointer !important;
      transition: all 0.2s ease !important;
      box-shadow: 0 2px 12px rgba(56, 189, 248, 0.35) !important;
      white-space: nowrap !important;
    }}
    .nav-login-pill-btn:hover {{
      transform: translateY(-1px) !important;
      box-shadow: 0 4px 20px rgba(56, 189, 248, 0.55) !important;
      background: linear-gradient(135deg, #60c8f5 0%, #a78bfa 100%) !important;
      color: #0b0f19 !important;
    }}
    /* HIDDEN SPA BUTTONS */
    div[data-testid="stHorizontalBlock"]:has([class*="st-key-btn_nav_"]),
    div[class*="st-key-btn_nav_"], div[class*="st-key-btn_lang_"], div[class*="st-key-btn_act_"],
    div[class*="st-key-btn_nav_"] button, div[class*="st-key-btn_lang_"] button,
    div[class*="st-key-btn_act_"] button {{
      position: fixed !important;
      left: -9999px !important;
      top: -9999px !important;
      width: 1px !important;
      height: 1px !important;
      opacity: 0.001 !important;
      margin: 0 !important;
      padding: 0 !important;
      overflow: hidden !important;
      pointer-events: auto !important;
      border: none !important;
    }}
    /* GOOGLE SIGN-IN BUTTON */
    #google-signin-btn-slot {{
      background-color: #ffffff !important;
      border: 2px solid #0ea5e9 !important;
      border-radius: 9999px !important;
      box-shadow: 0 4px 18px rgba(14, 165, 233, 0.25) !important;
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
      overflow: hidden !important;
      transition: all 0.2s ease !important;
      box-sizing: border-box !important;
      width: 100% !important;
      max-width: 100% !important;
    }}
    #corebox-google-btn {{
      width: 100% !important;
      max-width: 100% !important;
      box-sizing: border-box !important;
    }}
    #google-signin-btn-slot:hover {{
      border-color: #38bdf8 !important;
      box-shadow: 0 6px 24px rgba(56, 189, 248, 0.42) !important;
    }}
    #google-signin-btn-slot iframe, .g_id_signin iframe,
    iframe[src*="accounts.google.com"] {{
      background: #ffffff !important;
      border: none !important;
      border-radius: 9999px !important;
      color-scheme: light !important;
      display: block !important;
    }}
    #loading-screen {{
      position: fixed;
      inset: 0;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      background: radial-gradient(circle at 50% 30%, #1e293b 0%, #0b0f19 80%);
      z-index: 99999;
      transition: opacity 0.5s ease-out;
      padding: 1.5rem;
      text-align: center;
      box-sizing: border-box;
    }}
    .glow-title {{
      font-size: clamp(2.4rem, 6vw, 3.5rem);
      font-weight: 800;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 0.5rem;
      text-shadow: 0 0 40px rgba(56, 189, 248, 0.4);
    }}
    .glow-subtitle {{
      color: #94a3b8;
      font-size: clamp(1rem, 3.5vw, 1.25rem);
      font-weight: 500;
      margin-bottom: 2rem;
      text-align: center;
      max-width: 520px;
      line-height: 1.5;
    }}
    .spinner-ring {{
      width: 48px;
      height: 48px;
      border: 4px solid rgba(56, 189, 248, 0.2);
      border-top-color: #38bdf8;
      border-radius: 50%;
      animation: spin 1s linear infinite;
    }}
    @keyframes spin {{
      to {{ transform: rotate(360deg); }}
    }}
    .load-text {{
      margin-top: 1.2rem;
      color: #64748b;
      font-size: 0.9rem;
    }}
    #root {{
      min-height: 100vh;
    }}
  </style>
</head>
<body>
  <div id="loading-screen">
    <div class="glow-title">📦 Corebox</div>
    <div class="glow-subtitle">Đơn giản hóa công việc của bạn.</div>
    <div class="spinner-ring"></div>
    <div class="load-text" id="load-status">Khởi tạo môi trường Cloudflare Pages...</div>
  </div>

  <div id="root"></div>

  <script>
    const bundledFiles = {files_json};

    // Instant Google OAuth 2.0 Hash / Query Token Detection (Zero Reload)
    (function() {{
      try {{
        let tok = null;
        let hash = window.location.hash;
        if (hash && (hash.includes("id_token=") || hash.includes("access_token="))) {{
          if (hash.startsWith("#")) hash = hash.substring(1);
          const params = new URLSearchParams(hash);
          tok = params.get("id_token");
        }}
        if (!tok) {{
          const urlParams = new URLSearchParams(window.location.search);
          tok = urlParams.get("g_token") || urlParams.get("id_token");
        }}
        if (tok) {{
          const parts = tok.split('.');
          if (parts.length === 3) {{
            const b64 = parts[1].replace(/-/g, '+').replace(/_/g, '/');
            const jsonStr = decodeURIComponent(atob(b64).split('').map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)).join(''));
            const payload = JSON.parse(jsonStr);
            const email = (payload.email || '').toLowerCase().trim();
            const name = payload.name || email.split('@')[0];
            if (email) {{
              const isAdmin = (email === "happyclone96@gmail.com");
              const userObj = {{ email: email, name: name }};
              localStorage.setItem("corebox_active_user", JSON.stringify(userObj));
              
              let uStore = JSON.parse(localStorage.getItem("corebox_users_store") || "{{}}");
              if (!uStore[email]) {{
                uStore[email] = {{
                  email: email,
                  full_name: name || email.split('@')[0],
                  role: isAdmin ? "admin" : "user",
                  status: isAdmin ? "active" : "pending",
                  created_at: new Date().toISOString().replace("T", " ").substring(0, 19),
                  updated_at: new Date().toISOString().replace("T", " ").substring(0, 19)
                }};
              }} else {{
                if (name) uStore[email].full_name = name;
              }}
              localStorage.setItem("corebox_users_store", JSON.stringify(uStore));
              
              // Async sync to Cloudflare KV
              fetch("/api/users", {{
                method: "POST",
                headers: {{ "Content-Type": "application/json" }},
                body: JSON.stringify({{ email: email, full_name: name, role: isAdmin ? "admin" : "user", status: isAdmin ? "active" : "pending" }})
              }}).catch(e => console.error("KV sync error:", e));

              // Clean URL without reloading
              const cleanUrl = new URL(window.location.href);
              cleanUrl.hash = "";
              cleanUrl.searchParams.delete("g_token");
              cleanUrl.searchParams.delete("id_token");
              cleanUrl.searchParams.set("page", "home");
              window.history.replaceState(null, "", cleanUrl.toString());
            }}
          }}
        }}
      }} catch (e) {{
        console.error("Instant OAuth token parse error:", e);
      }}
    }})();

    function findBtn(name) {{
      const keyElem = document.querySelector('.st-key-btn_' + name);
      if (keyElem) {{
        const b = keyElem.querySelector('button');
        if (b) return b;
      }}
      const btns = document.querySelectorAll('button');
      for (const b of btns) {{
        const t = (b.innerText || '').trim();
        if (t === name) return b;
        if (b.getAttribute('title') === name || b.getAttribute('help') === name) return b;
      }}
      return null;
    }}

    window.coreboxNav = function(page, lang, e) {{
      if (e) {{
        if (e.preventDefault) e.preventDefault();
        if (e.stopPropagation) e.stopPropagation();
      }}
      const url = new URL(window.location);
      if (page) url.searchParams.set("page", page);
      if (lang) url.searchParams.set("lang", lang);
      url.searchParams.delete("u");
      window.history.replaceState({{}}, "", url);
      
      const btn = findBtn('nav_' + page);
      if (btn) {{
        btn.click();
        return false;
      }}
      let retries = 0;
      const interval = setInterval(() => {{
        retries++;
        const rBtn = findBtn('nav_' + page);
        if (rBtn) {{
          clearInterval(interval);
          rBtn.click();
        }} else if (retries > 30) {{
          clearInterval(interval);
        }}
      }}, 30);
      return false;
    }};

    window.coreboxLang = function(newLang, e) {{
      if (e) {{
        if (e.preventDefault) e.preventDefault();
        if (e.stopPropagation) e.stopPropagation();
      }}
      const url = new URL(window.location);
      url.searchParams.set("lang", newLang);
      url.searchParams.delete("u");
      window.history.replaceState({{}}, "", url);

      const target = document.getElementById("google-signin-btn-slot");
      if (target) {{
        target.removeAttribute("data-rendered-locale");
        target.innerHTML = "";
      }}
      if (window.initGoogleSignIn) window.initGoogleSignIn();

      const btn = findBtn('lang_' + newLang);
      if (btn) {{
        btn.click();
        return false;
      }}
      let retries = 0;
      const interval = setInterval(() => {{
        retries++;
        const rBtn = findBtn('lang_' + newLang);
        if (rBtn) {{
          clearInterval(interval);
          rBtn.click();
        }} else if (retries > 30) {{
          clearInterval(interval);
        }}
      }}, 30);
      return false;
    }};

    window.coreboxAction = function(action, e) {{
      if (e) {{
        if (e.preventDefault) e.preventDefault();
        if (e.stopPropagation) e.stopPropagation();
      }}
      const url = new URL(window.location);
      url.searchParams.set("action", action);
      url.searchParams.delete("u");
      if (action === "logout") {{
        url.searchParams.delete("g_token");
        try {{ localStorage.removeItem("corebox_active_user"); }} catch(e) {{}}
      }}
      window.history.replaceState({{}}, "", url);
      const btn = findBtn('act_' + action);
      if (btn) {{
        btn.click();
        return false;
      }}
      let retries = 0;
      const interval = setInterval(() => {{
        retries++;
        const rBtn = findBtn('act_' + action);
        if (rBtn) {{
          clearInterval(interval);
          rBtn.click();
        }} else if (retries > 30) {{
          clearInterval(interval);
        }}
      }}, 30);
      return false;
    }};

    window.coreboxUpdateUserStatus = async function(email, status) {{
      if (!email) return;
      const e = email.toLowerCase().trim();
      const nowStr = new Date().toISOString().replace("T", " ").substring(0, 19);
      try {{
        let uStore = JSON.parse(localStorage.getItem("corebox_users_store") || "{{}}");
        if (uStore[e]) {{
          uStore[e].status = status;
          uStore[e].updated_at = nowStr;
          localStorage.setItem("corebox_users_store", JSON.stringify(uStore));
        }}
      }} catch (err) {{}}
      try {{
        await fetch("/api/users", {{
          method: "POST",
          headers: {{ "Content-Type": "application/json" }},
          body: JSON.stringify({{ action: "update_status", email: e, status: status }})
        }});
      }} catch (err) {{
        console.error("API update status error:", err);
      }}
    }};

    window.coreboxDeleteUser = async function(email) {{
      if (!email) return;
      const e = email.toLowerCase().trim();
      try {{
        let uStore = JSON.parse(localStorage.getItem("corebox_users_store") || "{{}}");
        delete uStore[e];
        localStorage.setItem("corebox_users_store", JSON.stringify(uStore));
      }} catch (err) {{}}
      try {{
        await fetch("/api/users", {{
          method: "POST",
          headers: {{ "Content-Type": "application/json" }},
          body: JSON.stringify({{ action: "delete", email: e }})
        }});
      }} catch (err) {{
        console.error("API delete user error:", err);
      }}
    }};

    window.coreboxSaveCatalog = async function(catalogJsonStr) {{
      if (!catalogJsonStr) return;
      try {{
        localStorage.setItem("corebox_catalog_store", catalogJsonStr);
      }} catch (err) {{}}
      try {{
        await fetch("/api/catalog", {{
          method: "POST",
          headers: {{ "Content-Type": "application/json" }},
          body: catalogJsonStr
        }});
      }} catch (err) {{
        console.error("API save catalog error:", err);
      }}
    }};

    window.handleGoogleCredentialResponse = async function(response) {{
      if (!response || !response.credential) return;
      let email = null;
      let name = null;
      try {{
        const parts = response.credential.split('.');
        if (parts.length === 3) {{
          const b64 = parts[1].replace(/-/g, '+').replace(/_/g, '/');
          const jsonStr = decodeURIComponent(atob(b64).split('').map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)).join(''));
          const payload = JSON.parse(jsonStr);
          email = (payload.email || '').toLowerCase().trim();
          name = payload.name || email.split('@')[0];
        }}
      }} catch (e) {{
        console.error("JWT parse error:", e);
      }}

      if (email) {{
        const isAdmin = (email === "happyclone96@gmail.com");
        // Save to localStorage active_user and users_store immediately
        try {{
          localStorage.setItem("corebox_active_user", JSON.stringify({{ email: email, name: name }}));
          let uStore = JSON.parse(localStorage.getItem("corebox_users_store") || "{{}}");
          if (!uStore[email]) {{
            uStore[email] = {{
              email: email,
              full_name: name || email.split('@')[0],
              role: isAdmin ? "admin" : "user",
              status: isAdmin ? "active" : "pending",
              created_at: new Date().toISOString().replace("T", " ").substring(0, 19),
              updated_at: new Date().toISOString().replace("T", " ").substring(0, 19)
            }};
          }} else {{
            if (name) uStore[email].full_name = name;
          }}
          localStorage.setItem("corebox_users_store", JSON.stringify(uStore));
        }} catch (e) {{}}

        // Send to Cloudflare KV via /api/users
        try {{
          await fetch("/api/users", {{
            method: "POST",
            headers: {{ "Content-Type": "application/json" }},
            body: JSON.stringify({{ email: email, full_name: name, role: isAdmin ? "admin" : "user", status: isAdmin ? "active" : "pending" }})
          }});
        }} catch (e) {{
          console.error("API user sync error:", e);
        }}
      }}

      const url = new URL(window.location);
      url.searchParams.set("page", "home");
      url.searchParams.delete("u");
      url.searchParams.set("g_token", response.credential);
      window.location.href = url.toString();
    }};

    window.initGoogleSignIn = function() {{
      try {{
        const url = new URL(window.location);
        const currentLang = url.searchParams.get("lang") || "vi";
        const gsiLocale = (currentLang === "en") ? "en" : "vi";

        if (window.google && window.google.accounts && window.google.accounts.id) {{
          window.google.accounts.id.initialize({{
            client_id: "806346687682-2u257o2r9r330c6n9so3f4uj1ntm5rcb.apps.googleusercontent.com",
            callback: window.handleGoogleCredentialResponse,
            auto_select: false,
            cancel_on_tap_outside: true,
            locale: gsiLocale
          }});
          const target = document.getElementById("google-signin-btn-slot");
          if (target && target.getAttribute("data-rendered-locale") !== gsiLocale) {{
            target.innerHTML = "";
            const btnWidth = Math.min(360, Math.max(280, Math.floor(window.innerWidth - 48)));
            window.google.accounts.id.renderButton(target, {{
              theme: "outline",
              size: "large",
              shape: "pill",
              text: "continue_with",
              logo_alignment: "left",
              width: btnWidth,
              locale: gsiLocale
            }});
            target.setAttribute("data-rendered-locale", gsiLocale);
          }}
          // Also show Google One Tap prompt if not logged in
          try {{
            const activeUser = localStorage.getItem("corebox_active_user");
            if (!activeUser) {{
              window.google.accounts.id.prompt();
            }}
          }} catch(e) {{}}
        }}
      }} catch (e) {{
        console.error("Google Identity Services error:", e);
      }}
    }};

    async function waitForStlite() {{
      let attempts = 0;
      while ((typeof stlite === "undefined" || !window.stlite) && attempts < 100) {{
        await new Promise(resolve => setTimeout(resolve, 100));
        attempts++;
      }}
      if (typeof stlite === "undefined" && !window.stlite) {{
        throw new Error("Không thể tải thư viện Stlite. Vui lòng kiểm tra kết nối mạng và tải lại trang.");
      }}
      return window.stlite || stlite;
    }}

    setInterval(() => {{
      const target = document.getElementById("google-signin-btn-slot");
      if (target) {{
        const url = new URL(window.location);
        const currentLang = url.searchParams.get("lang") || "vi";
        const gsiLocale = (currentLang === "en") ? "en" : "vi";
        if (target.getAttribute("data-rendered-locale") !== gsiLocale || !target.hasChildNodes()) {{
          window.initGoogleSignIn();
        }}
      }}
    }}, 400);

    window.addEventListener("load", async () => {{
      const loadStatus = document.getElementById("load-status");
      loadStatus.innerText = "Đang tải thư viện Python & Công cụ QLDA...";

      try {{
        const stliteLib = await waitForStlite();

        // Pre-mount sync: restore active session from localStorage
        try {{
          const activeSess = localStorage.getItem("corebox_active_user");
          if (activeSess) {{
            bundledFiles["active_session.json"] = activeSess;
          }}
        }} catch (e) {{}}

        // Pre-mount sync: fetch latest users and catalog from Cloudflare KV / localStorage
        try {{
          const fetchUsers = fetch("/api/users").then(r => r.ok ? r.json() : null).catch(() => null);
          const fetchCatalog = fetch("/api/catalog").then(r => r.ok ? r.json() : null).catch(() => null);
          const timeout = new Promise(resolve => setTimeout(resolve, 2000));

          const [usersRes, catRes] = await Promise.race([
            Promise.all([fetchUsers, fetchCatalog]),
            timeout.then(() => [null, null])
          ]);

          let usersStore = {{}};
          if (usersRes && usersRes.users) {{
            usersStore = usersRes.users;
            try {{ localStorage.setItem("corebox_users_store", JSON.stringify(usersStore)); }} catch(e){{}}
          }} else {{
            try {{ usersStore = JSON.parse(localStorage.getItem("corebox_users_store") || "{{}}"); }} catch(e){{}}
          }}
          if (usersStore && Object.keys(usersStore).length > 0) {{
            const uStr = JSON.stringify(usersStore);
            bundledFiles["users_store.json"] = uStr;
            bundledFiles["data/users.json"] = uStr;
          }}

          let catStore = null;
          if (catRes && catRes.catalog) {{
            catStore = catRes.catalog;
            try {{ localStorage.setItem("corebox_catalog_store", JSON.stringify(catStore)); }} catch(e){{}}
          }} else {{
            try {{ catStore = JSON.parse(localStorage.getItem("corebox_catalog_store") || "null"); }} catch(e){{}}
          }}
          if (catStore) {{
            const cStr = (typeof catStore === "string") ? catStore : JSON.stringify(catStore);
            bundledFiles["catalog_store.json"] = cStr;
            bundledFiles["data/catalog.json"] = cStr;
          }}
        }} catch (e) {{
          console.error("Pre-mount sync error:", e);
        }}

        stliteLib.mount({{
          requirements: [
            "openpyxl",
            "python-docx",
            "pandas",
            "xlsxwriter",
            "pypdf"
          ],
          entrypoint: "app.py",
          files: bundledFiles,
          streamlitConfig: {{
            "theme.base": "dark",
            "theme.primaryColor": "#38bdf8",
            "theme.backgroundColor": "#0b0f19",
            "theme.secondaryBackgroundColor": "#1e293b",
            "theme.textColor": "#f1f5f9"
          }}
        }}, document.getElementById("root"));

        // Hide loading screen once streamlit is mounted
        const checkReady = setInterval(() => {{
          const appElement = document.querySelector(".stApp");
          if (appElement) {{
            clearInterval(checkReady);
            const loader = document.getElementById("loading-screen");
            loader.style.opacity = "0";
            setTimeout(() => loader.remove(), 500);
          }}
        }}, 300);

      }} catch (err) {{
        loadStatus.innerHTML = "Lỗi khởi chạy: " + err.message + '<br><button onclick="window.location.reload()" style="margin-top:12px;padding:8px 18px;border-radius:8px;background:#38bdf8;color:#0b0f19;font-weight:700;border:none;cursor:pointer;">Tải lại trang</button>';
        console.error(err);
      }}
    }});
  </script>
</body>
</html>
"""

    # Write to public/index.html (for Cloudflare Pages with build output 'public')
    public_index = os.path.join(public_dir, "index.html")
    with open(public_index, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generated Cloudflare Pages distribution: {public_index}")

    # Also copy _worker.js and _routes.json to public/ if present
    import shutil
    for fn in ["_worker.js", "_routes.json"]:
        src = os.path.join(base_dir, fn)
        dst = os.path.join(public_dir, fn)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"Copied {fn} to {public_dir}")

    # Also write to root index.html (in case user configures Pages with root directory)
    root_index = os.path.join(base_dir, "index.html")
    with open(root_index, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generated root index.html: {root_index}")

if __name__ == "__main__":
    build_pages_app()
