import textwrap
import streamlit as st
import config
from auth import get_current_user, get_current_user_email, is_admin, is_active, is_pending
from i18n import t

def render_top_navbar(lang: str, current_page: str = "home"):
    """
    Renders the custom pure hover navbar:
    - 📦Corebox: Icon 📦 is separated, slightly larger than text. Clicking always goes to home.
    - 'Tools ⌵' and 'Administrator ⌵': Hover dropdowns, no white borders, left-aligned.
      * For Guest and Pending users: All functions are locked (🔒) and disabled.
      * For Active users: Tools are accessible.
      * For Admin: Both Tools and Administrator are accessible.
    - Preserves user identity via 'u' query parameter on all links to prevent logout.
    - Embedded fast SPA navigation (< 40ms) without full browser reload.
    """
    current_user = get_current_user()
    current_email = get_current_user_email()
    user_is_admin = is_admin()
    user_is_active = is_active()
    user_is_pending = is_pending()
    user_is_guest = (current_user is None)

    u_param = f"&u={current_email}" if current_email else ""

    # Tools sub-items links
    if user_is_active:
        tools_repo_html = f'<a href="?page=repo&lang={lang}{u_param}" onclick="return window.coreboxNav(\'repo\', \'{lang}\', event)" target="_self" class="nav-sub-link">📁 {t("nav_repo", lang)}</a>'
        tools_inspect_html = f'<a href="?page=inspect&lang={lang}{u_param}" onclick="return window.coreboxNav(\'inspect\', \'{lang}\', event)" target="_self" class="nav-sub-link">🔍 {t("nav_inspection", lang)}</a>'
    else:
        tools_repo_html = f'<span class="nav-sub-link nav-sub-link-disabled" title="Chức năng bị khóa">📁 {t("nav_repo", lang)} 🔒</span>'
        tools_inspect_html = f'<span class="nav-sub-link nav-sub-link-disabled" title="Chức năng bị khóa">🔍 {t("nav_inspection", lang)} 🔒</span>'

    # Admin sub-item link
    if user_is_admin:
        admin_link_html = f'<a href="?page=users&lang={lang}{u_param}" onclick="return window.coreboxNav(\'users\', \'{lang}\', event)" target="_self" class="nav-sub-link">👥 {t("nav_users", lang)}</a>'
    else:
        admin_link_html = f'<span class="nav-sub-link nav-sub-link-disabled" title="Chức năng bị khóa">👥 {t("nav_users", lang)} 🔒</span>'

    # Current language text (Pure text: Vietnamese or English, no symbols)
    current_lang_display = "Vietnamese" if lang == "vi" else "English"

    # User Display vs Guest Display
    if current_user:
        raw_name = current_user.get("full_name") or current_email.split("@")[0]
        user_display_name = raw_name
        avatar_initial = (user_display_name[0] if user_display_name else "U").upper()
        role = current_user.get("role", "user")
        status = current_user.get("status", "pending")
        role_display = "👑 ADMIN" if user_is_admin else (f"🟢 {t('status_active', lang)}" if status == "active" else f"⏳ {t('status_pending', lang)}")

        if user_is_admin:
            admin_dropdown_item = f'<a href="?page=users&lang={lang}{u_param}" onclick="return window.coreboxNav(\'users\', \'{lang}\', event)" target="_self" class="nav-sub-link">👥 {t("nav_users", lang)}</a>'
        else:
            admin_dropdown_item = ""

        user_menu_html = f"""
        <div class="nav-dropdown-item">
          <span class="nav-dropdown-label" style="display:inline-flex; align-items:center; gap:0.5rem; background:rgba(255,255,255,0.04); padding:0.35rem 0.75rem; border-radius:9999px; border:1px solid rgba(255,255,255,0.1);">
            <span style="font-weight:600; font-size:0.88rem; color:#f1f5f9;">{user_display_name}</span>
            <span class="user-avatar-dot" style="width:24px; height:24px; border-radius:50%; background:linear-gradient(135deg, #38bdf8 0%, #818cf8 100%); color:#0b0f19; font-weight:700; font-size:0.75rem; display:inline-flex; align-items:center; justify-content:center;">{avatar_initial}</span>
            <span class="nav-arrow">⌵</span>
          </span>
          <div class="nav-dropdown-menu" style="right: 0; left: auto; min-width: 240px;">
            <div style="padding: 0.65rem 1.15rem; border-bottom: 1px solid rgba(255,255,255,0.08); font-size: 0.82rem; color: #94a3b8;">
              <div style="font-weight: 600; color: #f1f5f9; margin-bottom: 3px;">{current_email}</div>
              <div style="color: #38bdf8; font-size: 0.75rem; font-weight: 700;">{role_display}</div>
            </div>
            {admin_dropdown_item}
            <a href="?page=login&lang={lang}{u_param}" onclick="return window.coreboxNav('login', '{lang}', event)" target="_self" class="nav-sub-link">🌐 {t('btn_switch_google', lang)}</a>
            <a href="?page=home&lang={lang}&action=logout" onclick="return window.coreboxAction('logout', event)" target="_self" class="nav-sub-link" style="color: #f87171 !important;">🚪 {t('nav_logout', lang)}</a>
          </div>
        </div>
        """
    else:
        guest_text = t("nav_guest", lang)
        user_menu_html = f"""
        <div class="nav-dropdown-item">
          <span class="nav-dropdown-label" style="display:inline-flex; align-items:center; gap:0.45rem; background:rgba(255,255,255,0.05); padding:0.35rem 0.8rem; border-radius:9999px; border:1px solid rgba(255,255,255,0.12); cursor:pointer;">
            <span style="font-weight:600; font-size:0.88rem; color:#f1f5f9;">{guest_text}</span>
            <span style="width:24px; height:24px; border-radius:50%; background:linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%); color:#0b0f19; font-size:0.75rem; display:inline-flex; align-items:center; justify-content:center;">👤</span>
            <span class="nav-arrow">⌵</span>
          </span>
          <div class="nav-dropdown-menu" style="right: 0; left: auto; min-width: 170px;">
            <a href="?page=login&lang={lang}" onclick="return window.coreboxNav('login', '{lang}', event)" target="_self" class="nav-sub-link" style="color:#38bdf8 !important; font-weight:600;">➔ {t('nav_login_action', lang)}</a>
          </div>
        </div>
        """

    # Search Quick Links depending on permissions
    search_links_html = ""
    if user_is_active:
        search_links_html += f'<div style="padding:0.4rem 1.1rem; font-size:0.75rem; color:#94a3b8; font-weight:600; text-transform:uppercase;">{t("nav_tools", lang)}</div>'
        search_links_html += f'<a href="?page=repo&lang={lang}{u_param}" onclick="return window.coreboxNav(\'repo\', \'{lang}\', event)" target="_self" class="nav-sub-link">📁 {t("nav_repo", lang)}</a>'
        search_links_html += f'<a href="?page=inspect&lang={lang}{u_param}" onclick="return window.coreboxNav(\'inspect\', \'{lang}\', event)" target="_self" class="nav-sub-link">🔍 {t("nav_inspection", lang)}</a>'
        if user_is_admin:
            search_links_html += f'<a href="?page=users&lang={lang}{u_param}" onclick="return window.coreboxNav(\'users\', \'{lang}\', event)" target="_self" class="nav-sub-link">👥 {t("nav_users", lang)}</a>'
    else:
        search_links_html = f'<div style="padding:0.6rem 1.1rem; font-size:0.8rem; color:#94a3b8;">🔒 Vui lòng đăng nhập để mở khóa tính năng</div>'

    # Build unindented HTML with instant SPA router script
    navbar_html = f"""<div class="corebox-navbar-container">
<div class="nav-bar-row">
<div class="nav-left-zone">
<a href="?page=home&lang={lang}{u_param}" onclick="return window.coreboxNav('home', '{lang}', event)" target="_self" class="brand-link-wrapper">
<span class="brand-icon-box">📦</span>
<span class="brand-title-text">Corebox</span>
</a>
<div class="nav-dropdown-item">
<span class="nav-dropdown-label">{t('nav_tools', lang)} <span class="nav-arrow">⌵</span></span>
<div class="nav-dropdown-menu">
{tools_repo_html}
{tools_inspect_html}
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
{search_links_html}
</div>
</div>
<!-- Language Switcher Dropdown (Pure text Vietnamese / English, no icons) -->
<div class="nav-dropdown-item">
<span class="nav-dropdown-label">{current_lang_display} <span class="nav-arrow">⌵</span></span>
<div class="nav-dropdown-menu" style="min-width: 140px;">
<a href="?page={current_page}&lang=vi{u_param}" onclick="return window.coreboxLang('vi', event)" target="_self" class="nav-sub-link">Vietnamese</a>
<a href="?page={current_page}&lang=en{u_param}" onclick="return window.coreboxLang('en', event)" target="_self" class="nav-sub-link">English</a>
</div>
</div>
<!-- User / Guest Pill & Avatar -->
{user_menu_html}
</div>
</div>
</div>
<script>
(function() {{
  function findBtn(name) {{
    let keyElem = document.querySelector('.st-key-btn_' + name);
    if (keyElem) {{
      let b = keyElem.querySelector('button');
      if (b) return b;
    }}
    let allBtns = document.querySelectorAll('button');
    for (let b of allBtns) {{
      if (b.innerText && b.innerText.trim() === name) return b;
    }}
    return null;
  }}

  window.coreboxNav = function(page, lang, e) {{
    if (e && e.preventDefault) e.preventDefault();
    let url = new URL(window.location.href);
    if (page) url.searchParams.set("page", page);
    if (lang) url.searchParams.set("lang", lang);
    window.history.pushState({{}}, "", url.toString());

    let btn = findBtn('nav_' + page);
    if (btn) {{
      btn.click();
      return false;
    }}
    window.location.href = url.toString();
    return false;
  }};

  window.coreboxLang = function(newLang, e) {{
    if (e && e.preventDefault) e.preventDefault();
    let url = new URL(window.location.href);
    url.searchParams.set("lang", newLang);
    window.history.pushState({{}}, "", url.toString());

    let btn = findBtn('lang_' + newLang);
    if (btn) {{
      btn.click();
      return false;
    }}
    window.location.href = url.toString();
    return false;
  }};

  window.coreboxAction = function(action, e) {{
    if (e && e.preventDefault) e.preventDefault();
    let url = new URL(window.location.href);
    url.searchParams.set("action", action);
    if (action === "logout") {{
      url.searchParams.delete("u");
    }}
    window.history.pushState({{}}, "", url.toString());

    let btn = findBtn('act_' + action);
    if (btn) {{
      btn.click();
      return false;
    }}
    window.location.href = url.toString();
    return false;
  }};
}})();
</script>"""

    if hasattr(st, "html"):
        st.html(navbar_html)
    else:
        st.markdown(textwrap.dedent(navbar_html).strip(), unsafe_allow_html=True)
