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
    - Right Column: 'Welcome back', official Google Identity Services OAuth button, security notice, terms.
    """
    # Top Bar with Back Button
    safe_html(f"""
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
        {t('login_btn_back', lang)}
      </a>
    </div>
    """)

    col_left, col_space, col_right = st.columns([1.1, 0.15, 1.0])

    with col_left:
        # Left branding block styled like MapleTools reference in Image 1
        safe_html(f"""
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
            {t('login_brand_subtitle', lang)}
          </div>
          <div style="
            font-size: 0.95rem;
            color: #94a3b8;
            line-height: 1.6;
            margin-bottom: 3rem;
            max-width: 500px;
          ">
            {t('login_brand_desc', lang)}
          </div>

          <div style="font-size: 0.85rem; color: #64748b; line-height: 1.6; max-width: 480px;">
            {t('login_footnote', lang)}
          </div>
        </div>
        """)

    with col_right:
        safe_html(f"""
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
            {"Chào mừng bạn đến với" if lang == "vi" else "Welcome to"}
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

          <!-- Official Google Identity Services Container -->
          <script src="https://accounts.google.com/gsi/client" async defer></script>
          <script>
            window.handleGoogleCredentialResponse = window.handleGoogleCredentialResponse || function(response) {{
              if (!response || !response.credential) return;
              const url = new URL(window.location);
              url.searchParams.set("g_token", response.credential);
              url.searchParams.set("page", "home");
              window.location.href = url.toString();
            }};
          </script>
          <div id="g_id_onload"
               data-client_id="{config.GOOGLE_CLIENT_ID}"
               data-context="signin"
               data-ux_mode="popup"
               data-callback="handleGoogleCredentialResponse"
               data-auto_prompt="false"
               data-locale="{lang}">
          </div>
          
          <div class="google-btn-wrapper" style="
            margin: 1.5rem 0 2.2rem 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 100%;
          ">
            <div id="google-signin-btn-slot"
                 class="g_id_signin"
                 data-type="standard"
                 data-shape="pill"
                 data-theme="outline"
                 data-text="continue_with"
                 data-size="large"
                 data-logo_alignment="left"
                 data-width="400"
                 style="
                   min-width: 320px;
                   max-width: 100%;
                   display: inline-flex;
                   justify-content: center;
                   align-items: center;
                   border-radius: 9999px;
                   background-color: #ffffff;
                   border: 2px solid #0ea5e9;
                   box-shadow: 0 4px 18px rgba(14, 165, 233, 0.25);
                   overflow: hidden;
                   transition: all 0.2s ease;
                   box-sizing: border-box;
                 ">
            </div>
          </div>

          <!-- Terms & Privacy Policy footer notice with Google policy links -->
          <div style="
            margin-top: 1.2rem;
            font-size: 0.85rem;
            color: #94a3b8;
            line-height: 1.6;
            text-align: center;
            max-width: 380px;
          ">
            {t('login_terms_privacy', lang)}
          </div>
        </div>
        """)
