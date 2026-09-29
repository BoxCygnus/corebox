import datetime
import streamlit as st
import config
from auth import get_current_user, get_current_user_email, is_admin, logout_user, login_user
from i18n import t

def render_top_navbar(lang: str):
    """
    Renders the custom pure hover navbar:
    - Bold and larger 'Corebox' on the left
    - 'Tools ⌵' and 'Administrator ⌵' (No icons, NO white borders, hover dropdown, left-aligned children)
    - 'Ngôn ngữ ⌵' / 'Language ⌵' (Hover dropdown with Tiếng Việt / English)
    - Google account name + Google Avatar (Hover dropdown with account info & switch)
    - Real-time formatted date & time
    """
    current_user = get_current_user()
    current_email = get_current_user_email()
    user_is_admin = is_admin()

    now_str = datetime.datetime.now().strftime("%a %b %d %H:%M:%S")

    # Format user display name & initial
    if current_user:
        raw_name = current_user.get("full_name") or current_email.split("@")[0]
        user_display_name = raw_name
        avatar_initial = (user_display_name[0] if user_display_name else "U").upper()
        role = current_user.get("role", "user")
        status = current_user.get("status", "pending")
    else:
        user_display_name = t("nav_guest", lang)
        avatar_initial = "G"
        role = "guest"
        status = "none"

    # Admin sub-item link (or locked alert)
    if user_is_admin:
        admin_link_html = f'<a href="?page=users" target="_self" class="nav-sub-link">👥 {t("nav_users", lang)}</a>'
    else:
        admin_link_html = f'<span class="nav-sub-link" style="opacity:0.5; cursor:not-allowed;">🔒 {t("nav_users", lang)} ({t("nav_admin_badge", lang)})</span>'

    # Current language indicator
    current_lang_display = "Tiếng Việt" if lang == "vi" else "English"

    # Build HTML Navbar
    navbar_html = f"""
    <div class="corebox-navbar-container">
        <div class="nav-bar-row">
            <!-- LEFT: Corebox (Bold & Large) -> Tools ⌵ -> Administrator ⌵ -->
            <div class="nav-left-zone">
                <a href="?page=home" target="_self" class="brand-logo-text">Corebox</a>
                
                <!-- Tools Dropdown (Hover to open) -->
                <div class="nav-dropdown-item">
                    <span class="nav-dropdown-label">
                        {t('nav_tools', lang)} <span class="nav-arrow">⌵</span>
                    </span>
                    <div class="nav-dropdown-menu">
                        <a href="?page=repo" target="_self" class="nav-sub-link">📁 {t('nav_repo', lang)}</a>
                        <a href="?page=inspect" target="_self" class="nav-sub-link">🔍 {t('nav_inspection', lang)}</a>
                    </div>
                </div>

                <!-- Administrator Dropdown (Hover to open) -->
                <div class="nav-dropdown-item">
                    <span class="nav-dropdown-label">
                        {t('nav_admin', lang)} <span class="nav-arrow">⌵</span>
                    </span>
                    <div class="nav-dropdown-menu">
                        {admin_link_html}
                    </div>
                </div>
            </div>

            <!-- RIGHT: Date/Time -> Language ⌵ -> User Name + Avatar -->
            <div class="nav-right-zone">
                <div class="nav-date-time">{now_str}</div>

                <!-- Language Switcher Dropdown (Hover to open) -->
                <div class="nav-dropdown-item">
                    <span class="nav-dropdown-label">
                        🌐 {current_lang_display} <span class="nav-arrow">⌵</span>
                    </span>
                    <div class="nav-dropdown-menu" style="min-width: 150px;">
                        <a href="?lang=vi" target="_self" class="nav-sub-link">🇻🇳 Tiếng Việt</a>
                        <a href="?lang=en" target="_self" class="nav-sub-link">🇬🇧 English</a>
                    </div>
                </div>

                <!-- Google Account & Avatar (Hover to open) -->
                <div class="nav-dropdown-item">
                    <span class="nav-dropdown-label">
                        <span>{user_display_name}</span>
                        <span class="user-avatar-dot">{avatar_initial}</span>
                        <span class="nav-arrow">⌵</span>
                    </span>
                    <div class="nav-dropdown-menu" style="right: 0; left: auto; min-width: 240px;">
                        <div style="padding: 0.6rem 1.15rem; border-bottom: 1px solid rgba(255,255,255,0.08); font-size: 0.82rem; color: #94a3b8;">
                            <div>{current_email or 'guest'}</div>
                            <div style="color: #4ade80; font-weight: 600; margin-top: 2px;">{status.upper()} ({role.upper()})</div>
                        </div>
                        <a href="?user=admin" target="_self" class="nav-sub-link">👑 {t('switch_account', lang)}: Admin</a>
                        <a href="?user=engineer" target="_self" class="nav-sub-link">⚡ {t('switch_account', lang)}: Kỹ sư</a>
                        <a href="?user=guest" target="_self" class="nav-sub-link">⏳ {t('switch_account', lang)}: Chờ duyệt</a>
                        <a href="?action=logout" target="_self" class="nav-sub-link" style="color: #f87171 !important;">🚪 {t('nav_logout', lang)}</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """

    st.markdown(navbar_html, unsafe_allow_html=True)
