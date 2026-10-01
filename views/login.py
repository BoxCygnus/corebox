import textwrap
import streamlit as st
import streamlit.components.v1 as components
import config
from i18n import t

def safe_html(html_str: str):
    clean_html = textwrap.dedent(html_str).strip()
    if hasattr(st, "html"):
        st.html(clean_html)
    else:
        st.markdown(clean_html, unsafe_allow_html=True)

def render_login_view(lang: str):
    """
    Renders modern Split-Screen Google Login View (Google Cloud Console OAuth 2.0):
    - Top Left: '← Back' button returning to home.
    - Left Column: Bold Corebox branding, subtitle, mascots, footer.
    - Right Column: 'Welcome back', official Google Identity Services OAuth button, security notice, terms.
    """
    btn_back_text = t("login_btn_back", lang)
    subtitle_text = t("login_brand_subtitle", lang)
    desc_text = t("login_brand_desc", lang)
    footnote_text = t("login_footnote", lang)
    welcome_text = "Chào mừng bạn đến với" if lang == "vi" else "Welcome to"
    terms_text = t("login_terms_privacy", lang)
    client_id = config.GOOGLE_CLIENT_ID

    # Top Bar with Back Button
    top_html = """
    <div style="margin-bottom: 2rem; padding: 0.5rem 0;">
      <a href="?page=home&lang={lang}" onclick="return window.coreboxNav('home', '{lang}', event)" target="_self" class="login-back-btn" style="
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        color: #94a3b8;
        text-decoration: none;
        font-size: 0.95rem;
        font-weight: 600;
        padding: 0.4rem 0.8rem;
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        transition: all 0.2s ease;
      ">
        {btn_back_text}
      </a>
    </div>
    """.format(lang=lang, btn_back_text=btn_back_text)
    safe_html(top_html)

    col_left, col_space, col_right = st.columns([1.1, 0.15, 1.0])

    with col_left:
        # Left branding block styled like MapleTools reference in Image 1
        left_html = """
        <div style="padding-top: 2rem; padding-right: 1.5rem;">
          <div class="hero-brand-name" style="
            font-size: 3.8rem;
            line-height: 1.1;
            margin-bottom: 1.2rem;
            display: inline-block;
          ">
            Corebox
          </div>
          <div style="
            font-size: 1.25rem;
            font-weight: 500;
            color: #cbd5e1;
            line-height: 1.6;
            margin-bottom: 1.5rem;
            max-width: 520px;
          ">
            {subtitle_text}
          </div>
          <div style="
            font-size: 0.95rem;
            color: #94a3b8;
            line-height: 1.6;
            margin-bottom: 3rem;
            max-width: 500px;
          ">
            {desc_text}
          </div>

          <div style="font-size: 0.85rem; color: #64748b; line-height: 1.6; max-width: 480px;">
            {footnote_text}
          </div>
        </div>
        """.format(subtitle_text=subtitle_text, desc_text=desc_text, footnote_text=footnote_text)
        safe_html(left_html)

    with col_right:
        top_right_html = """
        <div style="
          padding-top: 4rem;
          max-width: 440px;
          margin: 0 auto;
          text-align: center;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
        ">
          <div style="
            font-size: 2.1rem;
            font-weight: 700;
            color: #ffffff;
            letter-spacing: -0.02em;
            margin-bottom: 0.35rem;
            text-align: center;
          ">
            {welcome_text}
          </div>
          <div style="
            font-size: 2.75rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 35px rgba(56, 189, 248, 0.4);
            margin-bottom: 1.8rem;
            text-align: center;
          ">
            Corebox
          </div>
        </div>
        """.format(welcome_text=welcome_text)
        safe_html(top_right_html)

        # Standalone components.html guarantees reliable execution of Google Identity Services
        button_html = """
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="utf-8">
          <script src="https://accounts.google.com/gsi/client" async defer></script>
          <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
              background: transparent;
              display: flex;
              justify-content: center;
              align-items: center;
              overflow: hidden;
              width: 100%;
              min-height: 52px;
            }}
            .btn-wrapper {{
              display: inline-flex;
              align-items: center;
              justify-content: center;
              padding: 2px;
              border-radius: 9999px;
              background-color: #ffffff;
              border: 2px solid #0ea5e9;
              box-shadow: 0 4px 18px rgba(14, 165, 233, 0.28);
              transition: all 0.2s ease;
            }}
            .btn-wrapper:hover {{
              border-color: #38bdf8;
              box-shadow: 0 6px 24px rgba(56, 189, 248, 0.45);
            }}
          </style>
        </head>
        <body>
          <div id="g_id_onload"
               data-client_id="{client_id}"
               data-context="signin"
               data-ux_mode="popup"
               data-callback="onGoogleAuth"
               data-auto_prompt="false"
               data-locale="{lang}">
          </div>
          <div class="btn-wrapper">
            <div class="g_id_signin"
                 data-type="standard"
                 data-shape="pill"
                 data-theme="outline"
                 data-text="continue_with"
                 data-size="large"
                 data-logo_alignment="left"
                 data-width="360">
            </div>
          </div>
          <script>
            function onGoogleAuth(response) {{
              if (!response || !response.credential) return;
              var token = encodeURIComponent(response.credential);
              try {{
                if (window.top && window.top.location && window.top.location.href.includes("pages.dev")) {{
                  var topUrl = new URL(window.top.location.href);
                  topUrl.searchParams.set("g_token", response.credential);
                  topUrl.searchParams.set("page", "home");
                  window.top.location.href = topUrl.toString();
                  return;
                }}
              }} catch(e) {{}}
              try {{
                var pUrl = new URL(window.parent.location.href);
                pUrl.searchParams.set("g_token", response.credential);
                pUrl.searchParams.set("page", "home");
                window.parent.location.href = pUrl.toString();
              }} catch(e) {{
                window.location.href = "?g_token=" + token + "&page=home";
              }}
            }}
          </script>
        </body>
        </html>
        """.format(client_id=client_id, lang=lang)
        components.html(button_html, height=65)

        bottom_right_html = """
        <div style="
          margin-top: 0.8rem;
          font-size: 0.85rem;
          color: #94a3b8;
          line-height: 1.6;
          text-align: center;
          max-width: 440px;
          margin-left: auto;
          margin-right: auto;
        ">
          {terms_text}
        </div>
        """.format(terms_text=terms_text)
        safe_html(bottom_right_html)
