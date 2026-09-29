import textwrap
import streamlit as st
import config
from i18n import t
from database import db
from auth import is_admin

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
    - Your project management, minus the manual hassle.
    - Data storage, automated inspection, and other supportive tools. (kích cỡ nhỏ hơn xíu)
    - Tất cả nội dung UI hiển thị trừ Tên phần mềm Corebox đều có bản dịch tiếng Việt khi đổi ngôn ngữ.
    """
    # Hero Box Layout
    safe_html(f"""<div class="hero-box">
<div class="hero-brand-name">Corebox</div>
<div class="hero-subheadline">{t('app_subtitle', lang)}</div>
<div class="hero-small-desc">{t('app_description', lang)}</div>
<div class="hero-cta-btn">
<a href="?page=inspect" target="_self">{t('explore_tools', lang)}</a>
</div>
</div>""")

    st.markdown("<br>", unsafe_allow_html=True)

    # Feature Action Cards (Song ngữ đầy đủ)
    col1, col2, col3 = st.columns(3)

    # Card 1: Data Repository
    with col1:
        safe_html(f"""<div class="feature-card">
<div class="feature-icon">📁</div>
<div class="feature-title">{t('home_card_repo_title', lang)}</div>
<div class="feature-desc">{t('home_card_repo_desc', lang)}</div>
</div>""")
        st.write("")
        safe_html(f"""<div style="text-align: center;">
<a href="?page=repo" target="_self" style="
display: block;
width: 100%;
padding: 0.55rem 1rem;
background: rgba(56, 189, 248, 0.1);
color: #38bdf8;
border: 1px solid rgba(56, 189, 248, 0.3);
border-radius: 8px;
text-decoration: none;
font-weight: 600;
font-size: 0.9rem;
box-sizing: border-box;
transition: all 0.2s ease;
">🚀 {t('btn_go', lang)}: {t('nav_repo', lang)}</a>
</div>""")

    # Card 2: Work Code Inspection
    with col2:
        safe_html(f"""<div class="feature-card">
<div class="feature-icon">🔍</div>
<div class="feature-title">{t('home_card_inspect_title', lang)}</div>
<div class="feature-desc">{t('home_card_inspect_desc', lang)}</div>
</div>""")
        st.write("")
        safe_html(f"""<div style="text-align: center;">
<a href="?page=inspect" target="_self" style="
display: block;
width: 100%;
padding: 0.55rem 1rem;
background: rgba(251, 191, 36, 0.1);
color: #fbbf24;
border: 1px solid rgba(251, 191, 36, 0.3);
border-radius: 8px;
text-decoration: none;
font-weight: 600;
font-size: 0.9rem;
box-sizing: border-box;
transition: all 0.2s ease;
">⚡ {t('btn_go', lang)}: {t('nav_inspection', lang)}</a>
</div>""")

    # Card 3: User Management
    with col3:
        safe_html(f"""<div class="feature-card">
<div class="feature-icon">👥</div>
<div class="feature-title">{t('home_card_admin_title', lang)}</div>
<div class="feature-desc">{t('home_card_admin_desc', lang)}</div>
</div>""")
        st.write("")
        if is_admin():
            safe_html(f"""<div style="text-align: center;">
<a href="?page=users" target="_self" style="
display: block;
width: 100%;
padding: 0.55rem 1rem;
background: rgba(168, 85, 247, 0.1);
color: #c084fc;
border: 1px solid rgba(168, 85, 247, 0.3);
border-radius: 8px;
text-decoration: none;
font-weight: 600;
font-size: 0.9rem;
box-sizing: border-box;
transition: all 0.2s ease;
">👑 {t('btn_go', lang)}: {t('nav_users', lang)}</a>
</div>""")
        else:
            safe_html(f"""<div style="text-align: center;">
<span style="
display: block;
width: 100%;
padding: 0.55rem 1rem;
background: rgba(255, 255, 255, 0.05);
color: #64748b;
border: 1px solid rgba(255, 255, 255, 0.08);
border-radius: 8px;
font-size: 0.9rem;
box-sizing: border-box;
cursor: not-allowed;
">🔒 {t('nav_users', lang)} (Admin)</span>
</div>""")

    # Footer (Song ngữ)
    safe_html(f"""<div class="corebox-footer">
{t('app_footer', lang)} • Cloudflare & Python Architecture • Version 2.0
</div>""")
