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
        margin: 0;
        padding: 0;
    }

    /* ELIMINATE TOP GAP COMPLETELY (Pull content flush to very top) */
    header,
    .stAppHeader,
    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    [data-testid="stDecoration"] {
        display: none !important;
        height: 0 !important;
        min-height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
        visibility: hidden !important;
    }

    /* HIDE STLITE LOADING TOASTS (Hình 4), REACT TOASTIFY & STREAMLIT STATUS WIDGET */
    .Toastify__toast-container,
    .Toastify__toast,
    .Toastify__toast--default,
    .Toastify__toast--info,
    [class*="Toastify"],
    .stlite-message,
    [data-testid="stStatusWidget"],
    .stStatusWidget,
    [data-testid="stToolbarActions"],
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    #MainMenu,
    .stDeployButton,
    div:has(> [data-testid="stStatusWidget"]),
    div[data-testid="stStatusWidget"] * {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        width: 0 !important;
        height: 0 !important;
        pointer-events: none !important;
        overflow: hidden !important;
    }

    /* HIDE HIDDEN SPA NAVIGATION CONTROLLER BUTTONS SAFELY (ALLOW JS .click()) */
    div[data-testid="stHorizontalBlock"]:has([class*="st-key-btn_nav_"]),
    div[class*="st-key-btn_nav_"],
    div[class*="st-key-btn_lang_"],
    div[class*="st-key-btn_act_"],
    div[class*="st-key-btn_nav_"] button,
    div[class*="st-key-btn_lang_"] button,
    div[class*="st-key-btn_act_"] button {
        position: fixed !important;
        top: -9999px !important;
        left: -9999px !important;
        width: 1px !important;
        height: 1px !important;
        opacity: 0.001 !important;
        overflow: hidden !important;
        margin: 0 !important;
        padding: 0 !important;
        border: none !important;
        pointer-events: auto !important;
    }

    /* Google Sign-in button: clean white background with sleek blue border */
    #google-signin-btn-slot {
        background-color: #ffffff !important;
        border: 2px solid #0ea5e9 !important;
        border-radius: 9999px !important;
        box-shadow: 0 4px 18px rgba(14, 165, 233, 0.25) !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        overflow: hidden !important;
        transition: all 0.2s ease !important;
        box-sizing: border-box !important;
    }

    #google-signin-btn-slot:hover {
        border-color: #38bdf8 !important;
        box-shadow: 0 6px 24px rgba(56, 189, 248, 0.42) !important;
    }

    #google-signin-btn-slot iframe,
    .g_id_signin iframe,
    iframe[src*="accounts.google.com"] {
        background: #ffffff !important;
        border: none !important;
        border-radius: 9999px !important;
        color-scheme: light !important;
        display: block !important;
    }

    /* Disabled Navigation Link for Guest & Pending Accounts */
    .nav-sub-link-disabled {
        opacity: 0.45 !important;
        cursor: not-allowed !important;
        pointer-events: none !important;
        color: #64748b !important;
    }

    [data-testid="stAppViewContainer"],
    [data-testid="stApp"],
    .stApp,
    section[data-testid="stMain"],
    section.main {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }

    /* 2CM MARGIN LEFT & RIGHT AT 100% DISPLAY (FLUSH AT TOP) */
    .main, 
    .main .block-container, 
    [data-testid="stMainBlockContainer"], 
    [data-testid="block-container"],
    div[data-testid="stAppViewBlockContainer"] {
        padding-top: 0 !important;
        padding-left: 2cm !important;
        padding-right: 2cm !important;
        padding-bottom: 0 !important;
        margin-top: 0 !important;
        margin-left: 0 !important;
        margin-right: 0 !important;
        max-width: 100% !important;
        width: 100% !important;
        box-sizing: border-box !important;
    }

    /* ============================================================== */
    /* CUSTOM TOP NAVBAR (Frozen / Sticky at top, flush under browser bar) */
    /* ============================================================== */
    .corebox-navbar-container {
        position: sticky !important;
        top: 0 !important;
        z-index: 999999 !important;
        background-color: #0b0e17 !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6) !important;
        padding-top: 0.45rem !important;
        padding-bottom: 0.45rem !important;
        margin-top: 0 !important;
        margin-bottom: 1rem !important;
        width: 100% !important;
        box-sizing: border-box !important;
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
        gap: 2.2rem;
    }

    /* Corebox Brand: Icon 📦 tách riêng, to hơn chữ 1 chút */
    .brand-link-wrapper {
        display: inline-flex !important;
        align-items: center !important;
        text-decoration: none !important;
        border: none !important;
        outline: none !important;
        cursor: pointer !important;
        gap: 0.4rem;
        padding-right: 0.8rem;
    }

    .brand-icon-box {
        font-size: 1.85rem !important;
        line-height: 1 !important;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        transition: transform 0.2s ease;
    }

    .brand-link-wrapper:hover .brand-icon-box {
        transform: scale(1.1);
    }

    .brand-title-text {
        font-size: 1.45rem !important;
        font-weight: 800 !important;
        color: #ffffff !important;
        letter-spacing: -0.02em;
        line-height: 1 !important;
        transition: color 0.15s ease;
    }

    .brand-link-wrapper:hover .brand-title-text {
        color: #38bdf8 !important;
    }

    /* Nav Dropdown on HOVER (Không cần bấm vào, chỉ chuột là mở) */
    .nav-dropdown-item {
        position: relative;
        display: inline-block;
        padding: 0.45rem 0;
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

    /* Dropdown Menu Container: Hiện ra khi hover (.nav-dropdown-item:hover) */
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

    /* Bordered Search Box for Functions (Khung search có viền) */
    .nav-search-bordered {
        display: flex;
        align-items: center;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.22);
        border-radius: 9999px;
        padding: 0.32rem 0.95rem;
        transition: all 0.2s ease;
        position: relative;
    }

    .nav-search-bordered:hover, .nav-search-bordered:focus-within {
        border-color: #38bdf8;
        background: rgba(255, 255, 255, 0.08);
        box-shadow: 0 0 14px rgba(56, 189, 248, 0.25);
    }

    .search-input-field {
        background: transparent !important;
        border: none !important;
        outline: none !important;
        color: #ffffff !important;
        font-size: 0.88rem !important;
        font-family: inherit !important;
        width: 175px;
        margin-left: 0.4rem;
    }

    .search-input-field::placeholder {
        color: #94a3b8;
        font-size: 0.85rem;
    }

    /* Quick jump search dropdown on hover/focus */
    .search-dropdown-results {
        display: none;
        position: absolute;
        top: 120%;
        left: 0;
        width: 250px;
        background: #111827;
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 10px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.7);
        padding: 0.4rem 0;
        z-index: 99999;
    }

    .nav-search-bordered:hover .search-dropdown-results,
    .nav-search-bordered:focus-within .search-dropdown-results {
        display: block;
        animation: menuFadeIn 0.15s ease-out forwards;
    }

    /* Right Group: Search, Language, Google Avatar */
    .nav-right-zone {
        display: flex;
        align-items: center;
        gap: 1.3rem;
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
        padding: 3.5rem 1rem 2.8rem 1rem;
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

    /* Subtitle: Đơn giản hóa hành trình chuyển đổi số của bạn */
    .hero-subheadline {
        font-size: 1.55rem;
        font-weight: 600;
        color: #f1f5f9;
        margin: 0 0 0.6rem 0;
        line-height: 1.35;
        letter-spacing: -0.01em;
    }

    /* Data storage, automated inspection, and other supportive tools. */
    .hero-small-desc {
        font-size: 1.05rem;
        color: #94a3b8;
        line-height: 1.6;
        margin: 0 auto 1.5rem auto;
        max-width: 650px;
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

    /* HOME PAGE FULL HEIGHT CONTAINER (Center hero, push footer to bottom) */
    .home-page-container {
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
        min-height: calc(100vh - 120px) !important;
        box-sizing: border-box !important;
    }

    /* FOOTER SÁT MÉP DƯỚI 1CM Ở MỨC 100% GIAO DIỆN */
    .corebox-footer {
        text-align: center;
        padding: 0.85rem 0 !important;
        margin-top: auto !important;
        margin-bottom: 1cm !important; /* Căn lề dưới đúng 1cm ở mức 100% */
        color: #64748b;
        font-size: 0.85rem;
        letter-spacing: 0.05em;
        border-top: 1px solid rgba(255, 255, 255, 0.06);
    }

    /* EXPANDER HEADER FONT (To hơn bên trong và in đậm) */
    [data-testid="stExpander"] details summary p,
    [data-testid="stExpander"] summary span,
    .streamlit-expanderHeader p {
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        color: #f8fafc !important;
        letter-spacing: -0.01em !important;
    }

    /* NAV LOGIN PILL BUTTON (Hiện khi chưa đăng nhập) */
    .nav-login-btn-wrapper {
        display: inline-flex;
        align-items: center;
    }

    .nav-login-pill-btn {
        display: inline-flex !important;
        align-items: center !important;
        gap: 0.45rem !important;
        padding: 0.38rem 1.1rem !important;
        border-radius: 9999px !important;
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%) !important;
        color: #0b0f19 !important;
        font-size: 0.9rem !important;
        font-weight: 700 !important;
        text-decoration: none !important;
        border: none !important;
        outline: none !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 12px rgba(56, 189, 248, 0.35) !important;
        letter-spacing: 0.01em !important;
        white-space: nowrap !important;
    }

    .nav-login-pill-btn:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 20px rgba(56, 189, 248, 0.55) !important;
        background: linear-gradient(135deg, #60c8f5 0%, #a78bfa 100%) !important;
        color: #0b0f19 !important;
    }

    /* GOOGLE LOGIN BUTTON: Full width fill the white background container */
    #google-signin-btn-slot {
        width: 100% !important;
        min-width: unset !important;
        max-width: 100% !important;
    }

    #corebox-google-btn {
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }
    </style>
    """
