import textwrap
import streamlit as st
import config
from i18n import t
from auth import login_user, get_current_user_email

def safe_html(html_str: str):
    clean_html = textwrap.dedent(html_str).strip()
    if hasattr(st, "html"):
        st.html(clean_html)
    else:
        st.markdown(clean_html, unsafe_allow_html=True)

def render_login_view(lang: str):
    """
    Renders modern Split-Screen Google Login View (matching reference UI):
    - Top Left: '← Back' button returning to previous screen / home.
    - Left Column: Bold Corebox branding, subtitle, 4 project mascots/tools, footer.
    - Right Column: 'Welcome back', Google Sign-In button, quick admin login, email entry, terms notice.
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

          <!-- Mascots / Feature icons row (like the 4 characters in Image 1) -->
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
        # Right login box (clean, modern, matching image 1)
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
        </div>
        """)

        # Fast 1-Click Admin Login Button (for convenient access)
        btn_quick_admin = st.button(
            f"{t('login_quick_admin', lang)}",
            type="primary",
            use_container_width=True,
            key="btn_quick_admin_login"
        )
        if btn_quick_admin:
            login_user(config.ADMIN_EMAIL, "Box (Admin)")
            st.session_state["current_page"] = "home"
            st.success(t("msg_login_admin_success", lang))
            st.rerun()

        st.markdown(f"""
        <div style="
          display: flex;
          align-items: center;
          text-align: center;
          margin: 1.5rem 0;
          color: #475569;
          font-size: 0.75rem;
          font-weight: 700;
          letter-spacing: 0.1em;
        ">
          <div style="flex: 1; height: 1px; background: rgba(255,255,255,0.08);"></div>
          <span style="padding: 0 0.8rem;">{t('login_or_divider', lang)}</span>
          <div style="flex: 1; height: 1px; background: rgba(255,255,255,0.08);"></div>
        </div>
        """, unsafe_allow_html=True)

        # Google Email Input Form
        with st.form("google_sign_in_form", clear_on_submit=False):
            input_email = st.text_input(
                t("enter_google_email", lang),
                placeholder=t("login_email_placeholder", lang),
                key="google_email_login_field"
            )
            submit_google = st.form_submit_button(
                f"🚀 {t('btn_continue_google', lang)}",
                type="secondary",
                use_container_width=True
            )

            if submit_google:
                if input_email and "@" in input_email:
                    clean_email = input_email.strip().lower()
                    user = login_user(clean_email)
                    if clean_email == config.ADMIN_EMAIL.strip().lower():
                        st.session_state["current_page"] = "home"
                        st.success(t("msg_login_admin_success", lang))
                        st.rerun()
                    else:
                        st.session_state["current_page"] = "home"
                        st.info(t("msg_login_user_pending", lang))
                        st.rerun()
                else:
                    st.error("Vui lòng nhập định dạng email hợp lệ (vd: yourname@gmail.com)!" if lang == "vi" else "Please enter a valid email address (e.g. yourname@gmail.com)!")

        # Terms & Privacy Policy footer notice
        safe_html(f"""
        <div style="
          margin-top: 1.8rem;
          font-size: 0.82rem;
          color: #64748b;
          line-height: 1.6;
          text-align: center;
          max-width: 440px;
        ">
          {t('login_terms_privacy', lang)}
        </div>
        """)
