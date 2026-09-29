import textwrap
import streamlit as st
import config
from auth import get_current_user, get_current_user_email, is_admin
from i18n import t

def render_top_navbar(lang: str):
    """
    Renders the custom pure hover navbar:
    - 📦Corebox: Icon 📦 is separated, slightly larger than text.
    - 'Tools ⌵' and 'Administrator ⌵': Hover dropdowns, no white borders, left-aligned.
    - Bordered search box for functions/tools (Khung search có viền).
    - Language switcher with hover dropdown.
    - Google account name + Google Avatar with hover dropdown.
    - Date/time is removed as requested.
    """
    current_user = get_current_user()
    current_email = get_current_user_email()
    user_is_admin = is_admin()

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

    # Admin sub-item link
    if user_is_admin:
        admin_link_html = f'<a href="?page=users" target="_self" class="nav-sub-link">👥 {t("nav_users", lang)}</a>'
    else:
        admin_link_html = f'<span class="nav-sub-link" style="opacity:0.5; cursor:not-allowed;">🔒 {t("nav_users", lang)} ({t("nav_admin_badge", lang)})</span>'

    # Current language indicator
    current_lang_display = "Tiếng Việt" if lang == "vi" else "English"

    # Build unindented HTML to avoid any Markdown code block interpretation
    navbar_html = f"""<div class="corebox-navbar-container">
<div class="nav-bar-row">
<div class="nav-left-zone">
<a href="?page=home" target="_self" class="brand-link-wrapper">
<span class="brand-icon-box">📦</span>
<span class="brand-title-text">Corebox</span>
</a>
<div class="nav-dropdown-item">
<span class="nav-dropdown-label">{t('nav_tools', lang)} <span class="nav-arrow">⌵</span></span>
<div class="nav-dropdown-menu">
<a href="?page=repo" target="_self" class="nav-sub-link">📁 {t('nav_repo', lang)}</a>
<a href="?page=inspect" target="_self" class="nav-sub-link">🔍 {t('nav_inspection', lang)}</a>
</div>
</div>
<div class="nav-dropdown-item">
<span class="nav-dropdown-label">{t('nav_admin', lang)} <span class="nav-arrow">⌵</span></span>
<div class="nav-dropdown-menu">
{admin_link_html}
</div>
</div>
</div>
<div class="nav-right-zone">
<!-- Bordered Search Box for Functions -->
<div class="nav-search-bordered">
<span>🔍</span>
<input type="text" class="search-input-field" placeholder="{t('nav_search_placeholder', lang)}">
<div class="search-dropdown-results">
<div style="padding:0.4rem 1.1rem; font-size:0.75rem; color:#94a3b8; font-weight:600; text-transform:uppercase;">{t('nav_tools', lang)}</div>
<a href="?page=repo" target="_self" class="nav-sub-link">📁 {t('nav_repo', lang)}</a>
<a href="?page=inspect" target="_self" class="nav-sub-link">🔍 {t('nav_inspection', lang)}</a>
<a href="?page=users" target="_self" class="nav-sub-link">👥 {t('nav_users', lang)}</a>
</div>
</div>
<!-- Language Switcher Dropdown -->
<div class="nav-dropdown-item">
<span class="nav-dropdown-label">🌐 {current_lang_display} <span class="nav-arrow">⌵</span></span>
<div class="nav-dropdown-menu" style="min-width: 150px;">
<a href="?lang=vi" target="_self" class="nav-sub-link">🇻🇳 Tiếng Việt</a>
<a href="?lang=en" target="_self" class="nav-sub-link">🇬🇧 English</a>
</div>
</div>
<!-- Google Account & Avatar -->
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
</div>"""

    if hasattr(st, "html"):
        st.html(navbar_html)
    else:
        st.markdown(textwrap.dedent(navbar_html).strip(), unsafe_allow_html=True)
