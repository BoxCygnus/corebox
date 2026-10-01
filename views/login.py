import textwrap
import streamlit as st
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
    - Right Column: 'Welcome to Corebox', official Google OAuth button, security notice, terms.
    """
    btn_back_text = t("login_btn_back", lang)
    subtitle_text = t("login_brand_subtitle", lang)
    desc_text = t("login_brand_desc", lang)
    footnote_text = t("login_footnote", lang)
    welcome_text = "Chào mừng bạn đến với" if lang == "vi" else "Welcome to"
    btn_label = "Tiếp tục bằng tài khoản Google" if lang == "vi" else "Continue with Google"
    terms_text = t("login_terms_privacy", lang)
    client_id = config.GOOGLE_CLIENT_ID

    # Top Bar with Back Button
    top_html = """
    <div style="margin-bottom: 2rem; padding: 0.5rem 0;">
      <a href="?page=home&lang=__LANG__" onclick="return window.coreboxNav('home', '__LANG__', event)" target="_self" class="login-back-btn" style="
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
        __BTN_BACK_TEXT__
      </a>
    </div>
    """.replace("__LANG__", lang).replace("__BTN_BACK_TEXT__", btn_back_text)
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
            __SUBTITLE_TEXT__
          </div>
          <div style="
            font-size: 0.95rem;
            color: #94a3b8;
            line-height: 1.6;
            margin-bottom: 3rem;
            max-width: 500px;
          ">
            __DESC_TEXT__
          </div>

          <div style="font-size: 0.85rem; color: #64748b; line-height: 1.6; max-width: 480px;">
            __FOOTNOTE_TEXT__
          </div>
        </div>
        """.replace("__SUBTITLE_TEXT__", subtitle_text).replace("__DESC_TEXT__", desc_text).replace("__FOOTNOTE_TEXT__", footnote_text)
        safe_html(left_html)

    with col_right:
        right_html = """
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
            __WELCOME_TEXT__
          </div>
          <div style="
            font-size: 2.75rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 35px rgba(56, 189, 248, 0.4);
            margin-bottom: 2rem;
            text-align: center;
          ">
            Corebox
          </div>

          <!-- Official Google OAuth 2.0 Web Flow Button (Never blocked by iframes) -->
          <div style="
            margin: 1.2rem 0 1.8rem 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 100%;
          ">
            <button type="button"
                    id="corebox-google-btn"
                    onclick="triggerGoogleOAuth()"
                    style="
                      display: inline-flex;
                      align-items: center;
                      justify-content: center;
                      gap: 12px;
                      width: 360px;
                      max-width: 100%;
                      height: 48px;
                      padding: 0 20px;
                      border-radius: 9999px;
                      background-color: #ffffff;
                      border: 2px solid #0ea5e9;
                      box-shadow: 0 4px 18px rgba(14, 165, 233, 0.28);
                      color: #1e293b;
                      font-size: 15px;
                      font-weight: 600;
                      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                      cursor: pointer;
                      transition: all 0.2s ease;
                      outline: none;
                      user-select: none;
                    ">
              <svg width="20" height="20" viewBox="0 0 24 24" style="flex-shrink: 0;">
                <path fill="#4285F4" d="M23.745 12.27c0-.7-.06-1.4-.19-2.07H12v4.51h6.6c-.29 1.52-1.14 2.8-2.4 3.66v3.05h3.88c2.27-2.09 3.665-5.17 3.665-9.15z"/>
                <path fill="#34A853" d="M12 24c3.24 0 5.95-1.08 7.93-2.91l-3.88-3.05c-1.08.72-2.45 1.16-4.05 1.16-3.12 0-5.77-2.1-6.72-4.93H1.26v3.13C3.26 21.36 7.33 24 12 24z"/>
                <path fill="#FBBC05" d="M5.28 14.27c-.25-.72-.38-1.49-.38-2.27s.13-1.55.38-2.27V6.6H1.26C.46 8.22 0 10.05 0 12s.46 3.78 1.26 5.4l4.02-3.13z"/>
                <path fill="#EA4335" d="M12 4.75c1.77 0 3.35.61 4.6 1.8l3.42-3.42C17.95 1.19 15.24 0 12 0 7.33 0 3.26 2.64 1.26 6.6l4.02 3.13c.95-2.83 3.6-4.98 6.72-4.98z"/>
              </svg>
              <span>__BTN_LABEL__</span>
            </button>
          </div>

          <!-- Terms & Privacy Policy footer notice with Google policy links -->
          <div style="
            margin-top: 1rem;
            font-size: 0.85rem;
            color: #94a3b8;
            line-height: 1.6;
            text-align: center;
            max-width: 440px;
            margin-left: auto;
            margin-right: auto;
          ">
            __TERMS_TEXT__
          </div>
        </div>

        <script>
          function triggerGoogleOAuth() {
            var clientId = "__CLIENT_ID__";
            var topHost = window.location.hostname;
            try {
              if (window.top && window.top.location && window.top.location.hostname) {
                topHost = window.top.location.hostname;
              }
            } catch(e) {}

            var isPagesDev = topHost.includes("pages.dev");
            var redirectUri = isPagesDev ? "https://corebox-project.pages.dev" : "https://corebox.streamlit.app";
            var nonce = Math.random().toString(36).substring(2);
            var oauthUrl = "https://accounts.google.com/o/oauth2/v2/auth"
              + "?client_id=" + encodeURIComponent(clientId)
              + "&redirect_uri=" + encodeURIComponent(redirectUri)
              + "&response_type=token%20id_token"
              + "&scope=" + encodeURIComponent("openid email profile")
              + "&nonce=" + nonce
              + "&prompt=select_account";

            try {
              if (window.top && window.top.location) {
                window.top.location.href = oauthUrl;
                return;
              }
            } catch(e) {}
            window.location.href = oauthUrl;
          }
        </script>
        """.replace("__WELCOME_TEXT__", welcome_text).replace("__BTN_LABEL__", btn_label).replace("__TERMS_TEXT__", terms_text).replace("__CLIENT_ID__", client_id)
        safe_html(right_html)
