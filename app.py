import streamlit as st
import config
from styles import get_custom_css
from i18n import t
from auth import (
    get_current_user,
    get_current_user_email,
    is_admin,
    is_active,
    is_pending,
    login_user,
    logout_user,
    verify_and_login_google_token
)
from navbar import render_top_navbar
from views.home import render_home_view
from views.pending import render_pending_view
from views.users import render_users_view
from views.repository import render_repository_view
from views.inspection import render_inspection_view
from views.login import render_login_view

# Streamlit Page Configuration
st.set_page_config(
    page_title="Corebox - Project Management",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply Custom CSS styling
st.markdown(get_custom_css(), unsafe_allow_html=True)

# -----------------------------------------------------------------
# Hidden SPA Navigation Controllers (Triggered by client-side JS in <40ms)
# -----------------------------------------------------------------
c_nav = st.container()
with c_nav:
    st.markdown('<div id="corebox-nav-anchor" style="display:none;"></div>', unsafe_allow_html=True)
    col_h1, col_h2, col_h3, col_h4, col_h5, col_h6, col_h7, col_h8, col_h9 = st.columns(9)
    with col_h1:
        if st.button("nav_home", key="btn_nav_home", help="nav_home"):
            st.session_state["current_page"] = "home"
            try: st.query_params["page"] = "home"
            except Exception: pass
    with col_h2:
        if st.button("nav_repo", key="btn_nav_repo", help="nav_repo"):
            st.session_state["current_page"] = "repo"
            try: st.query_params["page"] = "repo"
            except Exception: pass
    with col_h3:
        if st.button("nav_inspect", key="btn_nav_inspect", help="nav_inspect"):
            st.session_state["current_page"] = "inspect"
            try: st.query_params["page"] = "inspect"
            except Exception: pass
    with col_h4:
        if st.button("nav_users", key="btn_nav_users", help="nav_users"):
            st.session_state["current_page"] = "users"
            try: st.query_params["page"] = "users"
            except Exception: pass
    with col_h5:
        if st.button("nav_login", key="btn_nav_login", help="nav_login"):
            st.session_state["current_page"] = "login"
            try: st.query_params["page"] = "login"
            except Exception: pass
    with col_h6:
        if st.button("lang_vi", key="btn_lang_vi", help="lang_vi"):
            st.session_state["lang"] = "vi"
            try: st.query_params["lang"] = "vi"
            except Exception: pass
    with col_h7:
        if st.button("lang_en", key="btn_lang_en", help="lang_en"):
            st.session_state["lang"] = "en"
            try: st.query_params["lang"] = "en"
            except Exception: pass
    with col_h8:
        if st.button("act_login", key="btn_act_login", help="act_login"):
            st.session_state["current_page"] = "login"
            try: st.query_params["page"] = "login"
            except Exception: pass
    with col_h9:
        if st.button("act_logout", key="btn_act_logout", help="act_logout"):
            logout_user()
            st.session_state["current_page"] = "home"
            try: st.query_params["page"] = "home"
            except Exception: pass

# -----------------------------------------------------------------
# Handle URL Query Parameters & Session Synchronization
# -----------------------------------------------------------------
# Ensure current user is synchronized from session_state or query_params 'u'
current_email = get_current_user_email()
if current_email and "u" not in st.query_params:
    try:
        st.query_params["u"] = current_email
    except Exception:
        pass

# Only initialize current_page from query_params on initial load
if "current_page" not in st.session_state:
    q_page = st.query_params.get("page")
    if q_page and q_page in ["home", "repo", "inspect", "users", "login"]:
        st.session_state["current_page"] = q_page
    else:
        st.session_state["current_page"] = "home"

if "lang" not in st.session_state:
    q_lang = st.query_params.get("lang")
    if q_lang and q_lang in ["vi", "en"]:
        st.session_state["lang"] = q_lang
    else:
        st.session_state["lang"] = "vi"

q_action = st.query_params.get("action")
if q_action in ["google_login", "login"]:
    st.session_state["current_page"] = "login"
    try:
        del st.query_params["action"]
    except Exception:
        pass
elif q_action == "logout":
    logout_user()
    st.session_state["current_page"] = "home"
    try:
        st.query_params["page"] = "home"
        del st.query_params["action"]
    except Exception:
        pass

# Handle Google OAuth 2.0 token callback from Google Identity Services
g_token = st.query_params.get("g_token")
if g_token:
    user = verify_and_login_google_token(g_token)
    try:
        del st.query_params["g_token"]
    except Exception:
        pass
    if user:
        st.session_state["current_page"] = "home"
        st.query_params["page"] = "home"
        st.query_params["u"] = user["email"]
        st.rerun()

# Initialize Session Defaults
if "lang" not in st.session_state:
    st.session_state["lang"] = "vi"

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "home"

lang = st.session_state.get("lang", "vi")
current_page = st.session_state.get("current_page", "home")

# Render Top Hover Navigation Bar (except on dedicated login screen)
if current_page != "login":
    render_top_navbar(lang, current_page)

# -----------------------------------------------------------------
# Main Content View Routing
# -----------------------------------------------------------------
if current_page == "login":
    render_login_view(lang)
elif is_pending():
    # If the user is pending approval, lock tools and display pending notification view
    render_pending_view(lang)
elif current_page == "repo":
    if not is_active():
        st.warning(t("admin_access_hint", lang))
        st.session_state["current_page"] = "home"
        st.query_params["page"] = "home"
        st.rerun()
    else:
        render_repository_view(lang)
elif current_page == "inspect":
    if not is_active():
        st.warning(t("admin_access_hint", lang))
        st.session_state["current_page"] = "home"
        st.query_params["page"] = "home"
        st.rerun()
    else:
        render_inspection_view(lang)
elif current_page == "users":
    if is_admin():
        render_users_view(lang)
    else:
        st.warning(t("admin_access_hint", lang))
        st.session_state["current_page"] = "home"
        st.query_params["page"] = "home"
        st.rerun()
else:
    render_home_view(lang)
