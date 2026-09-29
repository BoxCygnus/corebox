# Custom styling and CSS for COREBOX Web Application

def get_custom_css() -> str:
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    /* Global reset & background */
    html, body, [class*="css"], [data-testid="stAppViewContainer"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: #0b0e17 !important;
        color: #f1f5f9;
    }

    [data-testid="stHeader"] {
        display: none !important;
    }

    .main .block-container {
        padding-top: 1rem !important;
        padding-bottom: 3rem !important;
        max-width: 1200px !important;
    }

    /* ============================================================== */
    /* CUSTOM TOP NAVBAR (No white borders, pure hover dropdowns)     */
    /* ============================================================== */
    .corebox-navbar-container {
        background-color: #0b0e17;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        padding: 0.6rem 0.5rem;
        margin-bottom: 2rem;
        position: relative;
        z-index: 1000;
    }

    .nav-bar-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        width: 100%;
    }

    .nav-left-zone {
        display: flex;
        align-items: center;
        gap: 2rem;
    }

    /* Corebox Brand: In đậm và to hơn */
    .brand-logo-text {
        font-size: 1.45rem !important;
        font-weight: 800 !important;
        color: #ffffff !important;
        text-decoration: none !important;
        letter-spacing: -0.02em;
        cursor: pointer;
        border: none !important;
        outline: none !important;
        background: transparent !important;
        transition: color 0.15s ease;
    }

    .brand-logo-text:hover {
        color: #38bdf8 !important;
    }

    /* Nav Dropdown on HOVER (Không cần bấm vào) */
    .nav-dropdown-item {
        position: relative;
        display: inline-block;
        padding: 0.4rem 0;
    }

    .nav-dropdown-label {
        font-size: 0.95rem;
        font-weight: 500;
        color: #cbd5e1;
        cursor: pointer;
        user-select: none;
        display: flex;
        align-items: center;
        gap: 0.3rem;
        text-decoration: none;
        border: none !important;
        outline: none !important;
        background: transparent !important;
        transition: color 0.15s ease;
    }

    .nav-dropdown-label:hover {
        color: #ffffff;
    }

    .nav-arrow {
        font-size: 0.72rem;
        color: #94a3b8;
    }

    /* Dropdown Menu Container: Hiện ra khi chỉ chuột vào (.nav-dropdown-item:hover) */
    .nav-dropdown-menu {
        display: none;
        position: absolute;
        top: 100%;
        left: 0;
        min-width: 220px;
        background: #111827;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
        padding: 0.4rem 0;
        z-index: 99999;
    }

    .nav-dropdown-item:hover .nav-dropdown-menu {
        display: block;
        animation: menuFadeIn 0.15s ease-out forwards;
    }

    @keyframes menuFadeIn {
        from { opacity: 0; transform: translateY(-4px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Mục con: Căn lề trái, tuyệt đối không có viền trắng */
    .nav-sub-link {
        display: block;
        width: 100%;
        padding: 0.65rem 1.15rem;
        font-size: 0.92rem;
        font-weight: 500;
        color: #cbd5e1 !important;
        text-decoration: none !important;
        text-align: left !important;
        border: none !important;
        outline: none !important;
        background: transparent !important;
        box-sizing: border-box;
        transition: all 0.15s ease;
    }

    .nav-sub-link:hover {
        background: rgba(255, 255, 255, 0.08) !important;
        color: #ffffff !important;
    }

    /* Right Group: Search, Date/Time, Language, Google Avatar */
    .nav-right-zone {
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }

    .nav-date-time {
        color: #94a3b8;
        font-size: 0.85rem;
        white-space: nowrap;
    }

    .nav-user-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        cursor: pointer;
        color: #cbd5e1;
        font-size: 0.95rem;
        font-weight: 500;
    }

    .user-avatar-dot {
        width: 26px;
        height: 26px;
        border-radius: 50%;
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
        color: #0f172a;
        font-weight: 700;
        font-size: 0.75rem;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 10px rgba(251, 191, 36, 0.35);
    }

    /* ============================================================== */
    /* HERO SECTION (Corebox lớn nổi bật, Subtitle, Description)     */
    /* ============================================================== */
    .hero-box {
        text-align: center;
        padding: 4.5rem 1rem 3rem 1rem;
        max-width: 860px;
        margin: 0 auto;
    }

    /* Corebox in đậm, font chữ nổi bật, kích thước to */
    .hero-brand-name {
        font-size: 4.2rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        background: linear-gradient(135deg, #38bdf8 0%, #60a5fa 35%, #818cf8 70%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0 0 0.8rem 0;
        text-shadow: 0 0 45px rgba(56, 189, 248, 0.35);
        display: inline-block;
        line-height: 1.1;
    }

    /* Your project management, minus the manual hassle. */
    .hero-subheadline {
        font-size: 1.55rem;
        font-weight: 600;
        color: #f1f5f9;
        margin: 0 0 0.6rem 0;
        line-height: 1.35;
        letter-spacing: -0.01em;
    }

    /* Data storage, automated inspection, and other supportive tools. (kích cỡ nhỏ hơn xíu) */
    .hero-small-desc {
        font-size: 1.05rem;
        color: #94a3b8;
        line-height: 1.6;
        margin: 0 auto 2.2rem auto;
        max-width: 650px;
    }

    /* Yellow/Amber Pill Button */
    .hero-cta-btn button,
    .hero-cta-btn a {
        background: #fbbf24 !important;
        color: #0f172a !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        border-radius: 9999px !important;
        padding: 0.7rem 2.2rem !important;
        border: none !important;
        box-shadow: 0 4px 20px rgba(251, 191, 36, 0.3) !important;
        transition: all 0.2s ease-in-out !important;
        display: inline-flex !important;
        align-items: center !important;
        gap: 0.5rem !important;
        text-decoration: none !important;
        cursor: pointer !important;
    }

    .hero-cta-btn button:hover,
    .hero-cta-btn a:hover {
        background: #f59e0b !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 25px rgba(251, 191, 36, 0.5) !important;
        color: #0f172a !important;
    }

    /* Feature Cards */
    .feature-card {
        background: rgba(18, 24, 38, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.6rem 1.4rem;
        transition: all 0.25s ease-in-out;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        height: 100%;
    }

    .feature-card:hover {
        transform: translateY(-4px);
        border-color: rgba(56, 189, 248, 0.4);
        box-shadow: 0 8px 30px rgba(56, 189, 248, 0.12);
    }

    .feature-icon {
        font-size: 2.2rem;
        margin-bottom: 0.75rem;
        display: inline-block;
    }

    .feature-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #f1f5f9;
        margin-bottom: 0.4rem;
    }

    .feature-desc {
        font-size: 0.88rem;
        color: #94a3b8;
        line-height: 1.5;
    }

    /* Metric cards in inspection */
    .metric-card {
        background: rgba(18, 24, 38, 0.75);
        border-radius: 12px;
        padding: 1.1rem;
        border: 1px solid rgba(255, 255, 255, 0.08);
        text-align: center;
    }
    
    .metric-val {
        font-size: 1.9rem;
        font-weight: 800;
        margin-top: 0.25rem;
    }

    .metric-val-success { color: #4ade80; }
    .metric-val-danger { color: #f87171; }
    .metric-val-info { color: #38bdf8; }

    /* Pending Notice Box */
    .pending-notice-box {
        background: rgba(18, 24, 38, 0.9);
        border: 1px solid rgba(251, 191, 36, 0.4);
        border-radius: 18px;
        padding: 2.2rem;
        margin: 2rem auto;
        max-width: 680px;
        text-align: center;
        box-shadow: 0 10px 35px rgba(251, 191, 36, 0.12);
    }

    .pending-notice-icon {
        font-size: 3.2rem;
        margin-bottom: 1rem;
    }

    .pending-notice-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #fbbf24;
        margin-bottom: 0.8rem;
    }

    .pending-notice-text {
        font-size: 1.05rem;
        line-height: 1.6;
        color: #e2e8f0;
    }

    /* Footer */
    .corebox-footer {
        text-align: center;
        padding: 3.5rem 0 1.5rem 0;
        color: #64748b;
        font-size: 0.88rem;
        letter-spacing: 0.05em;
        border-top: 1px solid rgba(255, 255, 255, 0.06);
        margin-top: 4rem;
    }
    </style>
    """
