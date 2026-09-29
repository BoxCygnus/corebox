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
    login_user
)
from navbar import render_top_navbar
from views.home import render_home_view
from views.pending import render_pending_view
from views.users import render_users_view
from views.repository import render_repository_view
from views.inspection import render_inspection_view

# Streamlit Page Configuration
st.set_page_config(
    page_title="COREBOX - Project Management",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply Custom CSS styling
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Initialize Session States
if "lang" not in st.session_state:
    st.session_state["lang"] = "vi"

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "home"

# Cloudflare Access Auto-Detection & Initial Session setup
current_email = get_current_user_email()
if not current_email:
    # Auto-login as default Admin for seamless local development
    login_user(config.ADMIN_EMAIL, "System Administrator")

lang = st.session_state.get("lang", "vi")
current_page = st.session_state.get("current_page", "home")

# Render Top Navigation Bar (Always visible)
render_top_navbar(lang)

# Check user status
if is_pending():
    # Show polite pending approval screen
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
