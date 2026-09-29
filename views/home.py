import streamlit as st
import config
from i18n import t
from database import db
from auth import is_admin

def render_home_view(lang: str):
    """
    Renders Main Dashboard screen matching the user's reference image:
    - Top headline:
        'Your project management,' (Large White Bold)
        'minus the manual hassle.' (Large Warm Gold Bold)
    - Subtitle: 'Data storage, automated inspection, and other supportive tools.'
    - Rounded amber/gold pill button: 'Explore the tools →' / 'Khám phá công cụ →'
    - Feature cards & Database status
    - Footer: 'Developed by Box'
    """
    # 2-Tone Hero Section (Matching MapleTools reference)
    st.markdown(
        f"""
        <div class="hero-container">
            <h1 class="hero-line-white">Your project management,</h1>
            <h1 class="hero-line-gold">minus the manual hassle.</h1>
            <div class="hero-subtext">
                {t('app_description', lang)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Centered CTA Button
    col_cta1, col_cta2, col_cta3 = st.columns([1.5, 2, 1.5])
    with col_cta2:
        st.markdown('<div class="hero-cta-btn" style="text-align:center;">', unsafe_allow_html=True)
        cta_label = "Khám phá công cụ →" if lang == "vi" else "Explore the tools →"
        if st.button(cta_label, key="hero_explore_btn", use_container_width=True):
            st.session_state["current_page"] = "inspect"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Feature Action Cards
    col1, col2, col3 = st.columns(3)

    # Card 1: Data Repository
    with col1:
        st.markdown(
            f"""
            <div class="feature-card">
                <div class="feature-icon">📁</div>
                <div class="feature-title">{t('home_card_repo_title', lang)}</div>
                <div class="feature-desc">{t('home_card_repo_desc', lang)}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.write("")
        if st.button(f"🚀 {t('btn_go', lang)}: {t('nav_repo', lang)}", key="home_btn_repo", use_container_width=True):
            st.session_state["current_page"] = "repo"
            st.rerun()

    # Card 2: Work Code Inspection
    with col2:
        st.markdown(
            f"""
            <div class="feature-card">
                <div class="feature-icon">🔍</div>
                <div class="feature-title">{t('home_card_inspect_title', lang)}</div>
                <div class="feature-desc">{t('home_card_inspect_desc', lang)}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.write("")
        if st.button(f"⚡ {t('btn_go', lang)}: {t('nav_inspection', lang)}", key="home_btn_inspect", use_container_width=True):
            st.session_state["current_page"] = "inspect"
            st.rerun()

    # Card 3: User Management
    with col3:
        st.markdown(
            f"""
            <div class="feature-card">
                <div class="feature-icon">👥</div>
                <div class="feature-title">{t('home_card_admin_title', lang)}</div>
                <div class="feature-desc">{t('home_card_admin_desc', lang)}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.write("")
        if is_admin():
            if st.button(f"👑 {t('btn_go', lang)}: {t('nav_users', lang)}", key="home_btn_users", use_container_width=True):
                st.session_state["current_page"] = "users"
                st.rerun()
        else:
            st.button(f"🔒 {t('nav_users', lang)} (Admin)", key="home_btn_users_disabled", use_container_width=True, disabled=True)

    # Footer
    st.markdown(
        f"""
        <div class="corebox-footer">
            {t('app_footer', lang)} • Built with Python & Cloudflare • Version 2.0
        </div>
        """,
        unsafe_allow_html=True
    )
