import streamlit as st
import config
from auth import get_current_user, get_current_user_email, is_admin, logout_user, login_user
from i18n import t

def render_top_navbar(lang: str):
    """
    Renders the responsive top navigation bar matching requirements:
    Left: 📦 Corebox -> Tools (dropdown) -> Administrator (dropdown)
    Right: Language switcher -> Google Account status / Avatar
    """
    current_user = get_current_user()
    current_email = get_current_user_email()
    user_is_admin = is_admin()

    # Container for Top Navbar
    with st.container():
        col_left, col_mid, col_right = st.columns([5, 1, 4], vertical_alignment="center")

        # ---- LEFT: 📦 Corebox -> Tools -> Administrator ----
        with col_left:
            subcol1, subcol2, subcol3 = st.columns([1.2, 1.2, 1.4], vertical_alignment="center")

            # 1. 📦 Corebox (Home button)
            with subcol1:
                is_home_active = st.session_state.get("current_page", "home") == "home"
                btn_type = "primary" if is_home_active else "secondary"
                if st.button("📦 Corebox", key="nav_btn_home", use_container_width=True, type=btn_type):
                    st.session_state["current_page"] = "home"
                    st.rerun()

            # 2. Tools (Dropdown Menu via Popover)
            with subcol2:
                with st.popover(f"🛠️ {t('nav_tools', lang)} ▾", use_container_width=True):
                    st.markdown(f"**{t('nav_tools', lang)}**")
                    if st.button(f"📁 {t('nav_repo', lang)}", key="nav_drop_repo", use_container_width=True):
                        st.session_state["current_page"] = "repo"
                        st.rerun()
                    if st.button(f"🔍 {t('nav_inspection', lang)}", key="nav_drop_inspect", use_container_width=True):
                        st.session_state["current_page"] = "inspect"
                        st.rerun()

            # 3. Administrator (Dropdown Menu via Popover)
            with subcol3:
                with st.popover(f"⚡ {t('nav_admin', lang)} ▾", use_container_width=True):
                    st.markdown(f"**{t('nav_admin', lang)}**")
                    if user_is_admin:
                        if st.button(f"👥 {t('nav_users', lang)}", key="nav_drop_users", use_container_width=True):
                            st.session_state["current_page"] = "users"
                            st.rerun()
                    else:
                        st.caption(f"🔒 {t('access_denied', lang, admin_email=config.ADMIN_EMAIL)}")
                        if st.button(f"👥 {t('nav_users', lang)}", key="nav_drop_users_denied", use_container_width=True, disabled=True):
                            pass

        # ---- RIGHT: Language Switcher & Google Avatar / Account Status ----
        with col_right:
            rcol_lang, rcol_user = st.columns([1.6, 2.4], vertical_alignment="center")

            # Language Switcher
            with rcol_lang:
                lang_choice = st.selectbox(
                    "🌐 Lang",
                    options=["vi", "en"],
                    format_func=lambda x: "🇻🇳 Tiếng Việt" if x == "vi" else "🇬🇧 English",
                    index=0 if lang == "vi" else 1,
                    key="lang_select_box",
                    label_visibility="collapsed"
                )
                if lang_choice != st.session_state.get("lang", "vi"):
                    st.session_state["lang"] = lang_choice
                    st.rerun()

            # Google Account & Status Avatar
            with rcol_user:
                if current_user:
                    email = current_user.get("email", "")
                    name = current_user.get("full_name") or email.split("@")[0]
                    role = current_user.get("role", "user")
                    status = current_user.get("status", "pending")
                    
                    if role == "admin" and email == config.ADMIN_EMAIL:
                        badge_label = f"👑 Admin ({name})"
                    elif status == "active":
                        badge_label = f"🟢 {name}"
                    else:
                        badge_label = f"⏳ {name} (Chờ duyệt)"

                    with st.popover(badge_label, use_container_width=True):
                        st.markdown(f"**{t('logged_in_as', lang, email=email)}**")
                        st.markdown(f"**{t('th_name', lang)}:** {name}")
                        st.markdown(f"**{t('th_role', lang)}:** `{role}`")
                        
                        if status == "active":
                            st.success(f"**{t('th_status', lang)}:** Active")
                        elif status == "pending":
                            st.warning(f"**{t('th_status', lang)}:** Pending Approval")
                        else:
                            st.error(f"**{t('th_status', lang)}:** {status}")

                        st.divider()
                        st.markdown(f"*{t('switch_account', lang)} / Test:*")
                        switch_opt = st.selectbox(
                            "Tài khoản mẫu",
                            options=[
                                f"Admin ({config.ADMIN_EMAIL})",
                                "Kỹ sư 1 (engineer.demo@gmail.com)",
                                "Người dùng mới (new.guest@gmail.com)",
                                "Tùy chỉnh khác..."
                            ],
                            key="quick_switch_select"
                        )
                        if st.button("Đăng nhập tài khoản này", key="btn_apply_switch"):
                            if "Admin" in switch_opt:
                                login_user(config.ADMIN_EMAIL, "Official Administrator")
                            elif "Kỹ sư 1" in switch_opt:
                                login_user("engineer.demo@gmail.com", "Nguyễn Văn Kỹ Sư")
                            elif "Người dùng mới" in switch_opt:
                                login_user("new.guest@gmail.com", "Guest User")
                            st.rerun()

                        if st.button(f"🚪 {t('nav_logout', lang)}", key="btn_logout_user", use_container_width=True):
                            logout_user()
                            st.rerun()
                else:
                    with st.popover(f"👤 {t('nav_guest', lang)}", use_container_width=True):
                        st.markdown(f"### {t('nav_login', lang)}")
                        st.info("Đăng nhập bằng tài khoản Google để tiếp tục:")
                        
                        preset_email = st.selectbox(
                            "Chọn tài khoản thử nghiệm hoặc nhập email Google:",
                            options=[
                                f"{config.ADMIN_EMAIL} (Quản trị viên)",
                                "engineer.demo@gmail.com (Người dùng mẫu)",
                                "new.guest@gmail.com (Người dùng mới chưa duyệt)",
                                "Nhập email khác..."
                            ],
                            key="login_preset_select"
                        )
                        
                        custom_email = ""
                        custom_name = ""
                        if "Nhập email khác" in preset_email:
                            custom_email = st.text_input("Nhập email Google của bạn:", placeholder="ten_cua_ban@gmail.com")
                            custom_name = st.text_input("Họ và tên hiển thị:", placeholder="Nguyễn Văn A")
                            
                        if st.button(f"🚀 {t('login_button', lang)}", key="btn_do_login", use_container_width=True):
                            if "Admin" in preset_email:
                                login_user(config.ADMIN_EMAIL, "Official Administrator")
                            elif "engineer" in preset_email:
                                login_user("engineer.demo@gmail.com", "Nguyễn Văn Kỹ Sư")
                            elif "new.guest" in preset_email:
                                login_user("new.guest@gmail.com", "Guest User")
                            elif custom_email:
                                login_user(custom_email, custom_name or custom_email.split("@")[0])
                            st.rerun()

    st.markdown("<hr style='margin-top:0.4rem; margin-bottom:1.5rem; opacity:0.15;'>", unsafe_allow_html=True)
