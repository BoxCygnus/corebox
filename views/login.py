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
          <div style="
            font-size: 3.8rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            color: #f59e0b;
            background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 60%, #ea580c 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            line-height: 1.1;
            margin-bottom: 1.2rem;
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
            margin-bottom: 3.5rem;
            max-width: 500px;
          ">
            {t('login_brand_desc', lang)}
          </div>

          <!-- Mascots / Feature icons row -->
          <div style="
            display: flex;
            align-items: center;
            gap: 2rem;
            margin-bottom: 1.5rem;
            padding: 1.2rem 1.4rem;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 16px;
            width: fit-content;
          ">
            <div style="text-align: center;">
              <div style="font-size: 2.2rem; filter: drop-shadow(0 4px 10px rgba(251,191,36,0.3));">📦</div>
              <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 4px; font-weight: 600;">Corebox</div>
            </div>
            <div style="text-align: center;">
              <div style="font-size: 2.2rem; filter: drop-shadow(0 4px 10px rgba(56,189,248,0.3));">📁</div>
              <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 4px; font-weight: 600;">Catalog</div>
            </div>
            <div style="text-align: center;">
              <div style="font-size: 2.2rem; filter: drop-shadow(0 4px 10px rgba(168,85,247,0.3));">🔍</div>
              <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 4px; font-weight: 600;">Inspect</div>
            </div>
            <div style="text-align: center;">
              <div style="font-size: 2.2rem; filter: drop-shadow(0 4px 10px rgba(74,222,128,0.3));">⚡</div>
              <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 4px; font-weight: 600;">Sync</div>
            </div>
          </div>

          <div style="font-size: 0.8rem; color: #64748b; line-height: 1.5; max-width: 480px;">
            {t('login_footnote', lang)}
          </div>
        </div>
        """)

    with col_right:
        # Right login box (clean, modern, authentic Google Cloud OAuth 2.0)
        auth_hint_text = (
            f"Xác thực bảo mật qua <b>Google Cloud Console</b>. Hệ thống tự động cấp quyền <b>Admin chính thức</b> cho tài khoản <code>{config.ADMIN_EMAIL}</code>. Các tài khoản Google khác sẽ được phân quyền Người dùng (chờ duyệt)."
            if lang == "vi" else
            f"Secured by <b>Google Cloud Console</b>. Official <b>Admin privileges</b> are automatically granted to <code>{config.ADMIN_EMAIL}</code>. Other Google accounts receive standard user privileges (pending approval)."
        )

        safe_html(f"""
        <div style="padding-top: 3.5rem; max-width: 440px;">
          <div style="
            font-size: 2rem;
            font-weight: 700;
            color: #ffffff;
            letter-spacing: -0.02em;
            margin-bottom: 0.4rem;
          ">
            {t('login_welcome_back', lang)}
          </div>
          <div style="
            font-size: 0.95rem;
            color: #94a3b8;
            margin-bottom: 2rem;
          ">
            {t('login_sync_subtitle', lang)}
          </div>

          <!-- Official Google Identity Services Container -->
          <div id="g_id_onload"
               data-client_id="{config.GOOGLE_CLIENT_ID}"
               data-context="signin"
               data-ux_mode="popup"
               data-callback="handleGoogleCredentialResponse"
               data-auto_prompt="false">
          </div>
          
          <div style="margin: 1.5rem 0; min-height: 50px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 0.8rem;">
            <!-- Slot for Google rendered standard button -->
            <div id="google-signin-btn-slot"></div>
            
            <!-- Standard GSI fallback signin button -->
            <div class="g_id_signin"
                 data-type="standard"
                 data-shape="rectangular"
                 data-theme="filled_blue"
                 data-text="continue_with"
                 data-size="large"
                 data-logo_alignment="left"
                 data-width="360">
            </div>
          </div>

          <!-- Security & Role info card -->
          <div style="
            background: rgba(56, 189, 248, 0.05);
            border: 1px solid rgba(56, 189, 248, 0.2);
            border-radius: 12px;
            padding: 1rem 1.2rem;
            font-size: 0.85rem;
            color: #94a3b8;
            line-height: 1.6;
            margin-top: 1.5rem;
          ">
            <div style="display: flex; align-items: flex-start; gap: 0.6rem;">
              <span style="font-size: 1.1rem; line-height: 1;">🔒</span>
              <div>{auth_hint_text}</div>
            </div>
          </div>

          <!-- Terms & Privacy Policy footer notice -->
          <div style="
            margin-top: 2rem;
            font-size: 0.82rem;
            color: #64748b;
            line-height: 1.6;
            text-align: center;
          ">
            {t('login_terms_privacy', lang)}
          </div>
        </div>
        """)
