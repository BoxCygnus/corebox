import textwrap
import streamlit as st
import config
from i18n import t
from auth import is_admin, is_pending
from views.pending import render_pending_view

def safe_html(html_str: str):
    """Renders HTML safely using st.html or unindented markdown."""
    clean_html = textwrap.dedent(html_str).strip()
    if hasattr(st, "html"):
        st.html(clean_html)
    else:
        st.markdown(clean_html, unsafe_allow_html=True)

def render_home_view(lang: str):
    """
    Renders Main Dashboard screen:
    - Corebox (In đậm, font chữ nổi bật, kích thước to)
    - Đơn giản hóa hành trình chuyển đổi số của bạn (Simplify your digital transformation journey)
    - Lưu trữ dữ liệu, kiểm tra tự động và các công cụ hỗ trợ.
    - Toàn bộ các ô truy cập nhanh đã được xóa bỏ theo yêu cầu.
    - Nếu tài khoản đang chờ phê duyệt, hiển thị thông báo chờ phê duyệt ngay tại đây.
    - Footer cách mép dưới 1cm.
    """
    if is_pending():
        render_pending_view(lang)
    else:
        # Hero Box Layout
        safe_html(f"""<div class="hero-box">
<div class="hero-brand-name">Corebox</div>
<div class="hero-subheadline">{t('app_subtitle', lang)}</div>
<div class="hero-small-desc">{t('app_description', lang)}</div>
</div>""")

    # Footer (Cách mép dưới màn hình 1cm)
    safe_html(f"""<div class="corebox-footer">
{t('app_footer', lang)} • Cloudflare & Python Architecture • Version 2.0
</div>""")
