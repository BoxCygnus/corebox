import streamlit as st
import config
from i18n import t
from auth import get_current_user_email, logout_user

def render_pending_view(lang: str):
    """
    Renders polite pending approval screen for new Google users:
    'Tài khoản của bạn đã đăng nhập thành công nhưng đang chờ Admin (happyclone96@gmail.com) phê duyệt. Vui lòng liên hệ quản trị viên.'
    """
    email = get_current_user_email() or "user@gmail.com"

    st.markdown(
        f"""
        <div class="pending-notice-box">
            <div class="pending-notice-icon">⏳</div>
            <div class="pending-notice-title">{t('pending_title', lang)}</div>
            <div class="pending-notice-text">
                {t('pending_message', lang, email=f"<b>{email}</b>", admin_email=f"<b>{config.ADMIN_EMAIL}</b>")}
            </div>
            <div style="margin-top:1.2rem; color:#94a3b8; font-size:0.9rem;">
                💡 {t('pending_tip', lang)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1.5, 2, 1.5])
    with col2:
        subc1, subc2 = st.columns(2)
        with subc1:
            if st.button("🔄 Tải lại trang", key="btn_reload_pending", use_container_width=True):
                st.rerun()
        with subc2:
            if st.button(f"🚪 {t('nav_logout', lang)}", key="btn_logout_pending", use_container_width=True):
                logout_user()
                st.rerun()
