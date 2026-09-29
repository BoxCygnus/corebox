import streamlit as st
import config
from i18n import t
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
        st.error(t("access_denied", lang, admin_email=config.ADMIN_EMAIL))
        st.info("Vui lòng đăng nhập với tài khoản Admin để truy cập khu vực này.")
        return

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

            with st.container(border=True):
                col_info, col_btn1, col_btn2 = st.columns([6, 2, 2], vertical_alignment="center")
                with col_info:
                    st.markdown(f"**👤 {u_name}** (`{u_email}`)")
                    st.caption(f"📅 {t('th_registered_at', lang)}: {u_time}")
                with col_btn1:
                    if st.button(f"✅ {t('btn_approve', lang)}", key=f"btn_app_{idx}_{u_email}", use_container_width=True, type="primary"):
                        db.update_user_status(u_email, "active")
                        st.success(t("msg_approved_success", lang, email=u_email))
                        st.rerun()
                with col_btn2:
                    if st.button(f"❌ {t('btn_reject', lang)}", key=f"btn_rej_{idx}_{u_email}", use_container_width=True):
                        db.update_user_status(u_email, "rejected")
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
                col_info, col_actions = st.columns([7, 3], vertical_alignment="center")
                with col_info:
                    badge_str = "👑 Admin Chính thức" if is_root_admin else ("⚡ Quản trị viên" if u_role == "admin" else "👤 Người dùng")
                    st.markdown(f"**{u_name}** (`{u_email}`) — *{badge_str}*")
                    st.caption(f"Cập nhật lần cuối: {u.get('updated_at', u.get('created_at', ''))}")
                with col_actions:
                    if not is_root_admin:
                        btn_c1, btn_c2 = st.columns(2)
                        with btn_c1:
                            if st.button("Tạm khóa", key=f"btn_lock_{idx}_{u_email}", use_container_width=True):
                                db.update_user_status(u_email, "pending")
                                st.rerun()
                        with btn_c2:
                            if st.button("Xóa", key=f"btn_del_{idx}_{u_email}", use_container_width=True):
                                db.delete_user(u_email)
                                st.rerun()
                    else:
                        st.badge("Hệ thống bảo vệ", icon="🔒")

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. REJECTED USERS (if any)
    rejected_users = db.get_all_users(status="rejected")
    if rejected_users:
        with st.expander(f"🚫 Danh sách tài khoản đã từ chối ({len(rejected_users)})"):
            for idx, u in enumerate(rejected_users):
                u_email = u["email"]
                col_a, col_b = st.columns([7, 3])
                with col_a:
                    st.write(f"• `{u_email}` ({u.get('full_name', '')})")
                with col_b:
                    if st.button("Khôi phục duyệt", key=f"btn_restore_{idx}_{u_email}"):
                        db.update_user_status(u_email, "active")
                        st.rerun()
