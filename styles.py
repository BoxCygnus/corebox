# Custom styling and CSS for COREBOX Web Application (Maple-Inspired Clean Dark Theme)

def get_custom_css() -> str:
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    /* Global reset & background */
    html, body, [class*="css"], [data-testid="stAppViewContainer"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: #0b0e17 !important;
        color: #f1f5f9;
    }

    [data-testid="stHeader"] {
        background: transparent !important;
    }

    /* ============================================================== */
    /* TOP NAVBAR (Border-free flat task items, bold Corebox)         */
    /* ============================================================== */

    /* Remove borders, backgrounds & shadows from all navbar buttons & popovers */
    .top-navbar-btn button,
    .top-navbar-btn [data-testid="stPopover"] > button,
    .top-navbar-btn [data-testid="baseButton-secondary"],
    .top-navbar-btn [data-testid="baseButton-primary"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: #cbd5e1 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        padding: 0.4rem 0.65rem !important;
        border-radius: 8px !important;
        transition: all 0.15s ease-in-out !important;
        height: auto !important;
        min-height: unset !important;
    }

    .top-navbar-btn button:hover,
    .top-navbar-btn [data-testid="stPopover"] > button:hover {
        background: rgba(255, 255, 255, 0.08) !important;
        color: #ffffff !important;
    }

    /* Corebox Brand Button: BOLD AND LARGER */
    .nav-brand-btn button,
    .nav-brand-btn [data-testid="baseButton-secondary"],
    .nav-brand-btn [data-testid="baseButton-primary"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: #ffffff !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 1.35rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em !important;
        padding: 0.2rem 0.5rem !important;
        display: flex !important;
        align-items: center !important;
    }

    .nav-brand-btn button:hover {
        background: transparent !important;
        color: #38bdf8 !important;
    }

    /* Navbar Search Pill Box */
    .nav-search-box {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 9999px;
        padding: 0.35rem 0.9rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        color: #94a3b8;
        font-size: 0.88rem;
    }
    .nav-search-shortcut {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 4px;
        padding: 0.1rem 0.35rem;
        font-size: 0.72rem;
        color: #cbd5e1;
    }

    /* Nav Divider */
    .nav-divider {
        color: rgba(255, 255, 255, 0.2);
        font-weight: 300;
        margin: 0 0.2rem;
        user-select: none;
    }

    /* Avatar styling */
    .user-avatar-circle {
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
        margin-left: 6px;
        vertical-align: middle;
        box-shadow: 0 0 10px rgba(251, 191, 36, 0.4);
    }

    /* ============================================================== */
    /* HERO SECTION (2-Tone Bold Title & Amber Pill CTA Button)       */
    /* ============================================================== */

    .hero-container {
        text-align: center;
        padding: 5rem 1rem 3.5rem 1rem;
        max-width: 860px;
        margin: 0 auto;
    }

    .hero-line-white {
        font-size: 3.8rem;
        font-weight: 800;
        color: #ffffff;
        line-height: 1.12;
        letter-spacing: -0.03em;
        margin: 0;
    }

    .hero-line-gold {
        font-size: 3.8rem;
        font-weight: 800;
        color: #fbbf24;
        line-height: 1.12;
        letter-spacing: -0.03em;
        margin: 0.35rem 0 1.2rem 0;
    }

    .hero-subtext {
        font-size: 1.15rem;
        color: #94a3b8;
        line-height: 1.6;
        margin-bottom: 2.2rem;
    }

    /* Yellow/Amber Pill Button */
    .hero-cta-btn button {
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
    }

    .hero-cta-btn button:hover {
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
        border-color: rgba(251, 191, 36, 0.35);
        box-shadow: 0 8px 30px rgba(251, 191, 36, 0.12);
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
