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
            margin-bottom: 1.8rem;
            text-align: center;
          ">
            {t('login_welcome_back', lang)}
          </div>

          <!-- Official Google Identity Services Container -->
          <div id="g_id_onload"
               data-client_id="{config.GOOGLE_CLIENT_ID}"
               data-context="signin"
               data-ux_mode="popup"
               data-callback="handleGoogleCredentialResponse"
               data-auto_prompt="false"
               data-locale="{lang}">
          </div>
          
          <div class="google-btn-wrapper" style="
            margin: 1rem 0 2rem 0;
            min-height: 54px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 100%;
          ">
            <!-- Google Sign-in Slot with Pill Shape styling like Image 5 -->
            <div id="google-signin-btn-slot" style="
              min-width: 340px;
              min-height: 52px;
              display: flex;
              justify-content: center;
              filter: drop-shadow(0 4px 14px rgba(0, 0, 0, 0.4));
            "></div>
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
