import streamlit as st
import config
from i18n import t
from database import db
from auth import is_admin, is_active, is_pending

def render_home_view(lang: str):
    """
    Renders Main Dashboard screen:
    - Glowing title COREBOX
    - Subtitle: 'Your project management, minus the manual hassle.'
    - Description: 'Data storage, automated inspection, and other supportive tools.'
    - Navigation cards & system status
    - Footer: 'Developed by Box'
    """
    # Glowing Hero Header
    st.markdown(
        f"""
        <div class="corebox-hero">
            <h1 class="corebox-title">{t('app_title', lang)}</h1>
            <div class="corebox-subtitle">"{t('app_subtitle', lang)}"</div>
            <div class="corebox-desc">{t('app_description', lang)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Quick Stats & Database Status Bar
    total_codes = db.count_work_codes()
    total_files = len(db.get_uploaded_files())
    backend_name = db.get_backend_name()

    stat_col1, stat_col2, stat_col3 = st.columns(3)
    with stat_col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div style="color:#94a3b8; font-size:0.85rem; font-weight:600;">{t('home_card_repo_title', lang)}</div>
                <div class="metric-val metric-val-info">{total_codes:,}</div>
                <div style="color:#64748b; font-size:0.75rem;">{total_files} {t('th_filename', lang).lower()}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with stat_col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div style="color:#94a3b8; font-size:0.85rem; font-weight:600;">{t('database_status', lang)}</div>
                <div class="metric-val metric-val-success" style="font-size:1.3rem; margin-top:0.6rem;">{backend_name}</div>
                <div style="color:#64748b; font-size:0.75rem;">Cloudflare D1 Ready</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with stat_col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div style="color:#94a3b8; font-size:0.85rem; font-weight:600;">Admin</div>
                <div class="metric-val metric-val-info" style="font-size:1.05rem; margin-top:0.75rem; word-break:break-all;">{config.ADMIN_EMAIL}</div>
                <div style="color:#64748b; font-size:0.75rem;">Primary Controller</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

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
