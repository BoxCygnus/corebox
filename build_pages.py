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
  <title>COREBOX — Project Management</title>
  <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>📦</text></svg>">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.73.1/build/stlite.css" />
  <script src="https://accounts.google.com/gsi/client" async defer></script>
  <style>
    body, html {{
      margin: 0;
      padding: 0;
      width: 100%;
      height: 100%;
      background-color: #0b0f19;
      color: #f1f5f9;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      overflow-x: hidden;
    }}
    [data-testid="stStatusWidget"],
    .stStatusWidget,
    [data-testid="stToolbarActions"],
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    #MainMenu,
    .stDeployButton {{
      display: none !important;
      visibility: hidden !important;
      opacity: 0 !important;
      height: 0 !important;
      width: 0 !important;
      pointer-events: none !important;
    }}
    div[data-testid="stHorizontalBlock"]:has([class*="st-key-btn_nav_"]),
    div[class*="st-key-btn_nav_"],
    div[class*="st-key-btn_lang_"],
    div[class*="st-key-btn_act_"],
    div[class*="st-key-btn_nav_"] button,
    div[class*="st-key-btn_lang_"] button,
    div[class*="st-key-btn_act_"] button {{
      position: absolute !important;
      left: -9999px !important;
      top: -9999px !important;
      width: 0 !important;
      height: 0 !important;
      opacity: 0 !important;
      visibility: hidden !important;
      margin: 0 !important;
      padding: 0 !important;
      overflow: hidden !important;
      pointer-events: auto !important;
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
    }}
    .glow-title {{
      font-size: 3.5rem;
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
      font-size: 1.1rem;
      margin-bottom: 2rem;
      text-align: center;
      max-width: 500px;
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
    <div class="glow-title">📦 COREBOX</div>
    <div class="glow-subtitle">"Your project management, minus the manual hassle."</div>
    <div class="spinner-ring"></div>
    <div class="load-text" id="load-status">Khởi tạo môi trường Cloudflare Pages...</div>
  </div>

  <div id="root"></div>

  <script src="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.73.1/build/stlite.js"></script>
  <script>
    const bundledFiles = {files_json};

    function findBtn(name) {{
      const keyElem = document.querySelector('.st-key-btn_' + name);
      if (keyElem) {{
        const b = keyElem.querySelector('button');
        if (b) return b;
      }}
      const btns = document.querySelectorAll('button');
      for (const b of btns) {{
        if (b.innerText && b.innerText.trim() === name) return b;
      }}
      return null;
    }}

    window.coreboxNav = function(page, lang, e) {{
      if (e && e.preventDefault) e.preventDefault();
      const url = new URL(window.location);
      if (page) url.searchParams.set("page", page);
      if (lang) url.searchParams.set("lang", lang);
      window.history.pushState({{}}, "", url);
      const btn = findBtn('nav_' + page);
      if (btn) {{
        btn.click();
        return false;
      }}
      window.location.href = url.toString();
      return false;
    }};

    window.coreboxLang = function(newLang, e) {{
      if (e && e.preventDefault) e.preventDefault();
      const url = new URL(window.location);
      url.searchParams.set("lang", newLang);
      window.history.pushState({{}}, "", url);
      const btn = findBtn('lang_' + newLang);
      if (btn) {{
        btn.click();
        return false;
      }}
      window.location.href = url.toString();
      return false;
    }};

    window.coreboxAction = function(action, e) {{
      if (e && e.preventDefault) e.preventDefault();
      const url = new URL(window.location);
      url.searchParams.set("action", action);
      window.history.pushState({{}}, "", url);
      const btn = findBtn('act_' + action);
      if (btn) {{
        btn.click();
        return false;
      }}
      window.location.href = url.toString();
      return false;
    }};

    window.handleGoogleCredentialResponse = function(response) {{
      if (!response || !response.credential) return;
      const url = new URL(window.location);
      url.searchParams.set("page", "home");
      url.searchParams.set("g_token", response.credential);
      window.location.href = url.toString();
    }};

    window.initGoogleSignIn = function() {{
      try {{
        if (window.google && window.google.accounts && window.google.accounts.id) {{
          window.google.accounts.id.initialize({{
            client_id: "806346687682-2u257o2r9r330c6n9so3f4uj1ntm5rcb.apps.googleusercontent.com",
            callback: window.handleGoogleCredentialResponse,
            auto_select: false,
            cancel_on_tap_outside: true
          }});
          const target = document.getElementById("google-signin-btn-slot");
          if (target && !target.hasChildNodes()) {{
            window.google.accounts.id.renderButton(target, {{
              theme: "filled_blue",
              size: "large",
              shape: "rectangular",
              text: "continue_with",
              logo_alignment: "left",
              width: 360
            }});
          }}
        }}
      }} catch (e) {{
        console.error("Google Identity Services error:", e);
      }}
    }};

    setInterval(() => {{
      const target = document.getElementById("google-signin-btn-slot");
      if (target && !target.hasChildNodes()) {{
        window.initGoogleSignIn();
      }}
    }}, 400);

    window.addEventListener("load", async () => {{
      const loadStatus = document.getElementById("load-status");
      loadStatus.innerText = "Đang tải thư viện Python & Công cụ QLDA...";

      try {{
        // Check if running on Cloudflare Access / Pages Functions to inject user email
        let cfUserEmail = null;
        try {{
          const res = await fetch("/api/user");
          if (res.ok) {{
            const data = await res.json();
            if (data.email) cfUserEmail = data.email;
          }}
        }} catch(e) {{}}

        stlite.mount({{
          requirements: [
            "openpyxl",
            "python-docx",
            "pandas",
            "xlsxwriter"
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
        loadStatus.innerText = "Lỗi khởi chạy: " + err.message;
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
    print(f"Generated Cloudflare Pages package: {public_index}")

    # Also write to root index.html (in case user configures Pages with root directory)
    root_index = os.path.join(base_dir, "index.html")
    with open(root_index, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generated root index.html: {root_index}")

if __name__ == "__main__":
    build_pages_app()
