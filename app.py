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

# Apply Custom CSS styling (Hover navbar, no white borders, refined hero)
st.markdown(get_custom_css(), unsafe_allow_html=True)

# -----------------------------------------------------------------
# Handle URL Query Parameters (from Hover Dropdown Navigation)
# -----------------------------------------------------------------
q_page = st.query_params.get("page")
if q_page and q_page in ["home", "repo", "inspect", "users"]:
    st.session_state["current_page"] = q_page

q_lang = st.query_params.get("lang")
if q_lang and q_lang in ["vi", "en"]:
    st.session_state["lang"] = q_lang

q_user = st.query_params.get("user")
if q_user == "admin":
    login_user(config.ADMIN_EMAIL, "Box")
elif q_user == "engineer":
    login_user("engineer.demo@gmail.com", "Nguyễn Kỹ Sư")
elif q_user == "guest":
    login_user("new.guest@gmail.com", "Guest User")

if st.query_params.get("action") == "logout":
    logout_user()

# Initialize Session Defaults
if "lang" not in st.session_state:
    st.session_state["lang"] = "vi"

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "home"

# Cloudflare Access Auto-Detection & Initial Session setup
current_email = get_current_user_email()
if not current_email:
    login_user(config.ADMIN_EMAIL, "Box")

lang = st.session_state.get("lang", "vi")
current_page = st.session_state.get("current_page", "home")

# Render Top Hover Navigation Bar
render_top_navbar(lang)

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
