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
# Handle URL Query Parameters & Session Synchronization
# -----------------------------------------------------------------
# Ensure query_params NEVER leak email into the browser URL
current_email = get_current_user_email()
if "u" in st.query_params:
    try:
        del st.query_params["u"]
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
        if "u" in st.query_params:
            del st.query_params["u"]
    except Exception:
        pass

# Handle Google OAuth 2.0 token callback from Google Identity Services or OAuth Web Flow
g_token = st.query_params.get("g_token") or st.query_params.get("id_token")
if g_token:
    user = verify_and_login_google_token(g_token)
    try:
        if "g_token" in st.query_params:
            del st.query_params["g_token"]
        if "id_token" in st.query_params:
            del st.query_params["id_token"]
    except Exception:
        pass
    if user:
        st.session_state["current_page"] = "home"
        st.query_params["page"] = "home"
        if "u" in st.query_params:
            try:
                del st.query_params["u"]
            except Exception:
                pass
        st.rerun()

# Client-side hash token detector for OAuth redirects
st.html("""
<script>
(function() {
  if (window.location.hash && window.location.hash.includes("id_token=")) {
    var p = new URLSearchParams(window.location.hash.substring(1));
    var tok = p.get("id_token");
    if (tok) {
      var u = new URL(window.location.href);
      u.hash = "";
      u.searchParams.set("g_token", tok);
      u.searchParams.set("page", "home");
      window.location.href = u.toString();
    }
  }
})();
</script>
""")

lang = st.session_state.get("lang", "vi")
current_page = st.session_state.get("current_page", "home")

# -----------------------------------------------------------------
# 1. RENDER TOP NAVBAR IMMEDIATELY (Very First Element in DOM, Flush at Top)
# -----------------------------------------------------------------
if current_page != "login":
    render_top_navbar(lang, current_page)

# -----------------------------------------------------------------
# 2. MAIN CONTENT VIEW ROUTING
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

# -----------------------------------------------------------------
# 3. HIDDEN SPA NAVIGATION CONTROLLERS (Rendered at bottom, zero top gap)
# -----------------------------------------------------------------
c_nav = st.container()
with c_nav:
    if st.button("nav_home", key="btn_nav_home", help="nav_home"):
        st.session_state["current_page"] = "home"
        try: st.query_params["page"] = "home"
        except Exception: pass
    if st.button("nav_repo", key="btn_nav_repo", help="nav_repo"):
        st.session_state["current_page"] = "repo"
        try: st.query_params["page"] = "repo"
        except Exception: pass
    if st.button("nav_inspect", key="btn_nav_inspect", help="nav_inspect"):
        st.session_state["current_page"] = "inspect"
        try: st.query_params["page"] = "inspect"
        except Exception: pass
    if st.button("nav_users", key="btn_nav_users", help="nav_users"):
        st.session_state["current_page"] = "users"
        try: st.query_params["page"] = "users"
        except Exception: pass
    if st.button("nav_login", key="btn_nav_login", help="nav_login"):
        st.session_state["current_page"] = "login"
        try: st.query_params["page"] = "login"
        except Exception: pass
    if st.button("lang_vi", key="btn_lang_vi", help="lang_vi"):
        st.session_state["lang"] = "vi"
        try: st.query_params["lang"] = "vi"
        except Exception: pass
    if st.button("lang_en", key="btn_lang_en", help="lang_en"):
        st.session_state["lang"] = "en"
        try: st.query_params["lang"] = "en"
        except Exception: pass
    if st.button("act_login", key="btn_act_login", help="act_login"):
        st.session_state["current_page"] = "login"
        try: st.query_params["page"] = "login"
        except Exception: pass
    if st.button("act_logout", key="btn_act_logout", help="act_logout"):
        logout_user()
        st.session_state["current_page"] = "home"
        try: st.query_params["page"] = "home"
        except Exception: pass
