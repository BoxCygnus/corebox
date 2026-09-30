import streamlit as st
import streamlit.components.v1 as components
import config
from i18n import t, format_datetime_by_lang
from database import db
from auth import is_admin, get_current_user_email

def render_users_view(lang: str):
    """
    Renders User Management page:
    - Exclusively accessible to Admin happyclone96@gmail.com
    - Displays Pending Approval Queue with [Phê duyệt] and [Từ chối] buttons
    - Lists active accounts with status and roles
    """
    if not is_admin():
        st.error(t("access_denied", lang))
        st.info(t("admin_access_hint", lang))
        return

    # Check for pending JS sync from previous action
    if "user_sync_js" in st.session_state and st.session_state["user_sync_js"]:
        js_code = st.session_state.pop("user_sync_js")
        components.html(f"<script>{js_code}</script>", height=0, width=0)

    st.markdown(f"## 👥 {t('user_mgmt_title', lang)}")
    st.caption(t('user_mgmt_desc', lang))
    st.divider()

    # 1. PENDING APPROVAL QUEUE
    pending_users = db.get_all_users(status="pending")
    st.markdown(f"### ⏳ {t('pending_users_section', lang, count=len(pending_users))}")

    if not pending_users:
        st.info(f"✨ {t('msg_no_pending', lang)}")
    else:
        for idx, u in enumerate(pending_users):
            u_email = u["email"]
            u_name = u["full_name"] or u_email.split("@")[0]
            u_time = u.get("created_at", "")
            formatted_u_time = format_datetime_by_lang(u_time, lang)

            with st.container(border=True):
                col_info, col_btn1, col_btn2 = st.columns([6, 2, 2], vertical_alignment="center")
                with col_info:
                    st.markdown(f"**👤 {u_name}** (`{u_email}`)")
                    st.caption(f"📅 {t('th_registered_at', lang)}: {formatted_u_time}")
                with col_btn1:
                    if st.button(f"✅ {t('btn_approve', lang)}", key=f"btn_app_{idx}_{u_email}", use_container_width=True, type="primary"):
                        db.update_user_status(u_email, "active")
                        st.session_state["user_sync_js"] = f"""
                        if (window.parent && window.parent.coreboxUpdateUserStatus) {{
                            window.parent.coreboxUpdateUserStatus('{u_email}', 'active');
                        }}
                        """
                        st.success(t("msg_approved_success", lang, email=u_email))
                        st.rerun()
                with col_btn2:
                    if st.button(f"❌ {t('btn_reject', lang)}", key=f"btn_rej_{idx}_{u_email}", use_container_width=True):
                        db.update_user_status(u_email, "rejected")
                        st.session_state["user_sync_js"] = f"""
                        if (window.parent && window.parent.coreboxUpdateUserStatus) {{
                            window.parent.coreboxUpdateUserStatus('{u_email}', 'rejected');
                        }}
                        """
                        st.warning(t("msg_rejected_success", lang, email=u_email))
                        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. ACTIVE USERS LIST
    active_users = db.get_all_users(status="active")
    st.markdown(f"### 🟢 {t('approved_users_section', lang, count=len(active_users))}")

    if active_users:
        for idx, u in enumerate(active_users):
            u_email = u["email"]
            u_name = u["full_name"] or u_email.split("@")[0]
            u_role = u.get("role", "user")
            is_root_admin = (u_email == config.ADMIN_EMAIL)

            with st.container(border=True):
                if not is_root_admin:
                    col_info, col_btn1, col_btn2 = st.columns([6, 2, 2], vertical_alignment="center")
                    with col_info:
                        badge_str = t("badge_admin", lang) if u_role == "admin" else t("badge_user", lang)
                        st.markdown(f"**{u_name}** (`{u_email}`) — *{badge_str}*")
                        formatted_updated = format_datetime_by_lang(u.get('updated_at', u.get('created_at', '')), lang)
                        st.caption(f"{t('last_updated_prefix', lang)}: {formatted_updated}")
                    with col_btn1:
                        if st.button(t("btn_suspend", lang), key=f"btn_lock_{idx}_{u_email}", use_container_width=True):
                            db.update_user_status(u_email, "pending")
                            st.session_state["user_sync_js"] = f"""
                            if (window.parent && window.parent.coreboxUpdateUserStatus) {{
                                window.parent.coreboxUpdateUserStatus('{u_email}', 'pending');
                            }}
                            """
                            st.rerun()
                    with col_btn2:
                        if st.button(t("btn_delete", lang), key=f"btn_del_{idx}_{u_email}", use_container_width=True):
                            db.delete_user(u_email)
                            st.session_state["user_sync_js"] = f"""
                            if (window.parent && window.parent.coreboxDeleteUser) {{
                                window.parent.coreboxDeleteUser('{u_email}');
                            }}
                            """
                            st.rerun()
                else:
                    col_info, col_lock = st.columns([8, 2], vertical_alignment="center")
                    with col_info:
                        badge_str = t("badge_root_admin", lang)
                        st.markdown(f"**{u_name}** — *{badge_str}*")
                        formatted_updated = format_datetime_by_lang(u.get('updated_at', u.get('created_at', '')), lang)
                        st.caption(f"{t('last_updated_prefix', lang)}: {formatted_updated}")
                    with col_lock:
                        st.markdown(
                            f'<span style="display:inline-flex; align-items:center; gap:4px; padding:0.25rem 0.65rem; border-radius:6px; background:rgba(56,189,248,0.12); color:#38bdf8; font-size:0.8rem; font-weight:600; border:1px solid rgba(56,189,248,0.25); white-space:nowrap;">🔒 {t("badge_protected", lang)}</span>',
                            unsafe_allow_html=True
                        )

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. REJECTED USERS (if any)
    rejected_users = db.get_all_users(status="rejected")
    if rejected_users:
        with st.expander(t("rejected_users_section", lang, count=len(rejected_users))):
            for idx, u in enumerate(rejected_users):
                u_email = u["email"]
                col_a, col_b = st.columns([7, 3])
                with col_a:
                    st.write(f"• `{u_email}` ({u.get('full_name', '')})")
                with col_b:
                    if st.button(t("btn_restore", lang), key=f"btn_restore_{idx}_{u_email}"):
                        db.update_user_status(u_email, "active")
                        st.session_state["user_sync_js"] = f"""
                        if (window.parent && window.parent.coreboxUpdateUserStatus) {{
                            window.parent.coreboxUpdateUserStatus('{u_email}', 'active');
                        }}
                        """
                        st.rerun()

