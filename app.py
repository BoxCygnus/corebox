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
    logout_user
)
from navbar import render_top_navbar
from views.home import render_home_view
from views.pending import render_pending_view
from views.users import render_users_view
from views.repository import render_repository_view
from views.inspection import render_inspection_view

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
    col_h1, col_h2, col_h3, col_h4, col_h5, col_h6, col_h7, col_h8 = st.columns(8)
    with col_h1:
        if st.button("nav_home", key="btn_nav_home", help="nav_home"):
            st.session_state["current_page"] = "home"
            st.rerun()
    with col_h2:
        if st.button("nav_repo", key="btn_nav_repo", help="nav_repo"):
            st.session_state["current_page"] = "repo"
            st.rerun()
    with col_h3:
        if st.button("nav_inspect", key="btn_nav_inspect", help="nav_inspect"):
            st.session_state["current_page"] = "inspect"
            st.rerun()
    with col_h4:
        if st.button("nav_users", key="btn_nav_users", help="nav_users"):
            st.session_state["current_page"] = "users"
            st.rerun()
    with col_h5:
        if st.button("lang_vi", key="btn_lang_vi", help="lang_vi"):
            st.session_state["lang"] = "vi"
            st.rerun()
    with col_h6:
        if st.button("lang_en", key="btn_lang_en", help="lang_en"):
            st.session_state["lang"] = "en"
            st.rerun()
    with col_h7:
        if st.button("act_login", key="btn_act_login", help="act_login"):
            st.session_state["show_google_login"] = True
            st.rerun()
    with col_h8:
        if st.button("act_logout", key="btn_act_logout", help="act_logout"):
            logout_user()
            st.session_state["show_google_login"] = False
            st.rerun()

# -----------------------------------------------------------------
# Handle URL Query Parameters (for initial deep links / bookmarking)
# -----------------------------------------------------------------
q_page = st.query_params.get("page")
if q_page and q_page in ["home", "repo", "inspect", "users"]:
    st.session_state["current_page"] = q_page

q_lang = st.query_params.get("lang")
if q_lang and q_lang in ["vi", "en"]:
    st.session_state["lang"] = q_lang

q_action = st.query_params.get("action")
if q_action in ["google_login", "login"]:
    st.session_state["show_google_login"] = True
elif q_action == "logout":
    logout_user()
    st.session_state["show_google_login"] = False

# Initialize Session Defaults
if "lang" not in st.session_state:
    st.session_state["lang"] = "vi"

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "home"

# Pre-install official Admin account happyclone96@gmail.com by default
current_email = get_current_user_email()
if not current_email:
    login_user(config.ADMIN_EMAIL, "Box")

lang = st.session_state.get("lang", "vi")
current_page = st.session_state.get("current_page", "home")

# Render Top Hover Navigation Bar
render_top_navbar(lang, current_page)

# -----------------------------------------------------------------
# Google Sign-In Modal / Card
# -----------------------------------------------------------------
if st.session_state.get("show_google_login", False):
    with st.container(border=True):
        col_g1, col_g2 = st.columns([8, 2], vertical_alignment="center")
        with col_g1:
            st.markdown(f"### 🌐 {t('google_login_title', lang)}")
            st.caption(t('google_login_desc', lang))
        with col_g2:
            if st.button(f"✕ {t('btn_cancel', lang)}", key="btn_close_login_modal", use_container_width=True):
                st.session_state["show_google_login"] = False
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        login_col1, login_col2 = st.columns([7, 3], vertical_alignment="bottom")
        with login_col1:
            input_email = st.text_input(
                t("enter_google_email", lang),
                placeholder="ten.nguoidung@gmail.com",
                key="google_email_input"
            )
        with login_col2:
            if st.button(f"🚀 {t('btn_continue_google', lang)}", type="primary", use_container_width=True, key="btn_submit_google_login"):
                if input_email and "@" in input_email:
                    clean_email = input_email.strip().lower()
                    login_user(clean_email)
                    st.session_state["show_google_login"] = False
                    if clean_email == config.ADMIN_EMAIL.strip().lower():
                        st.success(t("msg_login_admin_success", lang))
                    else:
                        st.info(t("msg_login_user_pending", lang))
                    st.rerun()
                else:
                    st.warning("Vui lòng nhập đúng định dạng địa chỉ email Google (@gmail.com).")
        st.divider()

# Check user status
if is_pending():
    render_pending_view(lang)
else:
    # Route to selected page
    if current_page == "home":
        render_home_view(lang)
    elif current_page == "repo":
        render_repository_view(lang)
    elif current_page == "inspect":
        render_inspection_view(lang)
    elif current_page == "users":
        render_users_view(lang)
    else:
        render_home_view(lang)
