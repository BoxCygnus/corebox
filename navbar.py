import datetime
import streamlit as st
import config
from auth import get_current_user, get_current_user_email, is_admin, logout_user, login_user
from i18n import t

def render_top_navbar(lang: str):
    """
    Renders the minimalist Maple-inspired Top Navigation Bar:
    - Bold and larger '📦 Corebox' on the top-left
    - 'Tools ⌵' and 'Administrator ⌵' (NO icons in front, border-free, same font & size)
    - Search bar in center
    - Right: Current date/time, Language switcher ('🌐 English ⌵' / '🌐 Tiếng Việt ⌵'),
             separator '|', and Google Account Name + Google Avatar.
    """
    current_user = get_current_user()
    current_email = get_current_user_email()
    user_is_admin = is_admin()

    now_str = datetime.datetime.now().strftime("%a %b %d %H:%M:%S")

    # Format user display name & avatar initial
    if current_user:
        raw_name = current_user.get("full_name") or current_email.split("@")[0]
        # Clean display name (take first word or short name)
        user_display_name = raw_name
        avatar_initial = (user_display_name[0] if user_display_name else "U").upper()
        role = current_user.get("role", "user")
        status = current_user.get("status", "pending")
    else:
        user_display_name = "Guest"
        avatar_initial = "G"
        role = "guest"
        status = "none"

    # Top Navbar Container
    with st.container():
        col_left, col_center, col_right = st.columns([4.2, 2.5, 4.3], vertical_alignment="center")

        # -------------------------------------------------------------
        # LEFT: 📦 Corebox (Bold & Larger) -> Tools ⌵ -> Administrator ⌵
        # -------------------------------------------------------------
        with col_left:
            nl1, nl2, nl3 = st.columns([1.6, 1.2, 1.5], vertical_alignment="center")

            # 1. 📦 Corebox (Home - In đậm và to hơn)
            with nl1:
                st.markdown('<div class="nav-brand-btn">', unsafe_allow_html=True)
                if st.button("📦 Corebox", key="nav_btn_home"):
                    st.session_state["current_page"] = "home"
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

            # 2. Tools ⌵ (Không biểu tượng ở trước, không viền, cùng cỡ chữ)
            with nl2:
                st.markdown('<div class="top-navbar-btn">', unsafe_allow_html=True)
                with st.popover(f"{t('nav_tools', lang)} ⌵", use_container_width=True):
                    st.markdown(f"**{t('nav_tools', lang)}**")
                    if st.button(t('nav_repo', lang), key="nav_drop_repo", use_container_width=True):
                        st.session_state["current_page"] = "repo"
                        st.rerun()
                    if st.button(t('nav_inspection', lang), key="nav_drop_inspect", use_container_width=True):
                        st.session_state["current_page"] = "inspect"
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

            # 3. Administrator ⌵ (Không biểu tượng ở trước, không viền, cùng cỡ chữ)
            with nl3:
                st.markdown('<div class="top-navbar-btn">', unsafe_allow_html=True)
                with st.popover(f"{t('nav_admin', lang)} ⌵", use_container_width=True):
                    st.markdown(f"**{t('nav_admin', lang)}**")
                    if user_is_admin:
                        if st.button(t('nav_users', lang), key="nav_drop_users", use_container_width=True):
                            st.session_state["current_page"] = "users"
                            st.rerun()
                    else:
                        st.caption(f"🔒 {t('access_denied', lang, admin_email=config.ADMIN_EMAIL)}")
                st.markdown('</div>', unsafe_allow_html=True)

        # -------------------------------------------------------------
        # CENTER: Search Pill (Matching reference image)
        # -------------------------------------------------------------
        with col_center:
            st.markdown(
                """
                <div class="nav-search-box">
                    <span>🔍 Search...</span>
                    <span class="nav-search-shortcut">⌘ K</span>
                </div>
                """,
                unsafe_allow_html=True
            )

        # -------------------------------------------------------------
        # RIGHT: Date/Time -> Language ⌵ -> | -> Google Name + Avatar
        # -------------------------------------------------------------
        with col_right:
            nr_time, nr_lang, nr_user = st.columns([1.8, 1.4, 1.8], vertical_alignment="center")

            # Date/Time
            with nr_time:
                st.markdown(
                    f"<div style='color:#94a3b8; font-size:0.85rem; white-space:nowrap; text-align:right;'>{now_str}</div>",
                    unsafe_allow_html=True
                )

            # Language Switcher (Không viền, chữ phẳng)
            with nr_lang:
                st.markdown('<div class="top-navbar-btn">', unsafe_allow_html=True)
                current_lang_label = "🌐 Tiếng Việt ⌵" if lang == "vi" else "🌐 English ⌵"
                with st.popover(current_lang_label, use_container_width=True):
                    if st.button("🇻🇳 Tiếng Việt", key="set_lang_vi", use_container_width=True):
                        st.session_state["lang"] = "vi"
                        st.rerun()
                    if st.button("🇬🇧 English", key="set_lang_en", use_container_width=True):
                        st.session_state["lang"] = "en"
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

            # Google Account & Avatar (Google Name + Avatar circle)
            with nr_user:
                st.markdown('<div class="top-navbar-btn">', unsafe_allow_html=True)
                user_button_label = f"{user_display_name} 🟡"
                with st.popover(user_button_label, use_container_width=True):
                    if current_user:
                        st.markdown(f"**{t('logged_in_as', lang, email=current_email)}**")
                        st.markdown(f"**{t('th_name', lang)}:** {user_display_name}")
                        st.markdown(f"**{t('th_role', lang)}:** `{role}`")
                        if status == "active":
                            st.success(f"**{t('th_status', lang)}:** Active")
                        elif status == "pending":
                            st.warning(f"**{t('th_status', lang)}:** Pending Approval")
                        
                        st.divider()
                        st.markdown(f"*{t('switch_account', lang)}:*")
                        switch_opt = st.selectbox(
                            "Chọn tài khoản thử nghiệm:",
                            options=[
                                f"Admin ({config.ADMIN_EMAIL})",
                                "Kỹ sư 1 (engineer.demo@gmail.com)",
                                "Người dùng mới (new.guest@gmail.com)",
                            ],
                            key="quick_switch_select"
                        )
                        if st.button("Chuyển tài khoản", key="btn_apply_switch"):
                            if "Admin" in switch_opt:
                                login_user(config.ADMIN_EMAIL, "Box")
                            elif "Kỹ sư 1" in switch_opt:
                                login_user("engineer.demo@gmail.com", "Nguyễn Kỹ Sư")
                            elif "Người dùng mới" in switch_opt:
                                login_user("new.guest@gmail.com", "Guest User")
                            st.rerun()

                        if st.button(f"🚪 {t('nav_logout', lang)}", key="btn_logout_user", use_container_width=True):
                            logout_user()
                            st.rerun()
                    else:
                        st.markdown(f"### {t('nav_login', lang)}")
                        st.info("Đăng nhập tài khoản Google:")
                        if st.button(f"🚀 Đăng nhập Admin ({config.ADMIN_EMAIL})", use_container_width=True):
                            login_user(config.ADMIN_EMAIL, "Box")
                            st.rerun()
                        if st.button("🚀 Đăng nhập Kỹ sư (Active)", use_container_width=True):
                            login_user("engineer.demo@gmail.com", "Nguyễn Kỹ Sư")
                            st.rerun()
                        if st.button("🚀 Đăng nhập Khách mới (Pending)", use_container_width=True):
                            login_user("new.guest@gmail.com", "Guest User")
                            st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

    # Bottom hairline border
    st.markdown("<hr style='margin-top:0.3rem; margin-bottom:1.5rem; border:none; border-bottom:1px solid rgba(255,255,255,0.08);'>", unsafe_allow_html=True)
