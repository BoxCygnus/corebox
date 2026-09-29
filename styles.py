# Custom styling and CSS for COREBOX Web Application

def get_custom_css() -> str:
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    /* Global reset and typography */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Corebox Glowing Brand Title */
    .corebox-hero {
        text-align: center;
        padding: 2.5rem 1rem 1.8rem 1rem;
        background: radial-gradient(circle at 50% 20%, rgba(30, 64, 175, 0.15) 0%, rgba(15, 23, 42, 0) 70%);
        border-radius: 20px;
        margin-bottom: 2rem;
        position: relative;
    }

    .corebox-title {
        font-size: 3.8rem;
        font-weight: 800;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        background: linear-gradient(135deg, #38bdf8 0%, #60a5fa 30%, #818cf8 70%, #c084fc 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shimmer 4s linear infinite;
        margin: 0;
        padding: 0;
        text-shadow: 0 0 35px rgba(56, 189, 248, 0.45);
        display: inline-block;
    }

    @keyframes shimmer {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .corebox-subtitle {
        font-size: 1.25rem;
        font-weight: 600;
        color: #94a3b8;
        margin-top: 0.75rem;
        letter-spacing: 0.02em;
    }

    .corebox-desc {
        font-size: 0.98rem;
        color: #64748b;
        margin-top: 0.35rem;
    }

    /* Feature Cards on Dashboard */
    .feature-card {
        background: rgba(30, 41, 59, 0.65);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 16px;
        padding: 1.6rem 1.4rem;
        transition: all 0.25s ease-in-out;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.18);
        height: 100%;
    }

    .feature-card:hover {
        transform: translateY(-4px);
        border-color: rgba(56, 189, 248, 0.45);
        box-shadow: 0 8px 30px rgba(56, 189, 248, 0.18);
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

    /* Badges */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.65rem;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.03em;
    }

    .badge-admin {
        background: rgba(168, 85, 247, 0.15);
        color: #c084fc;
        border: 1px solid rgba(168, 85, 247, 0.35);
    }

    .badge-active {
        background: rgba(34, 197, 94, 0.15);
        color: #4ade80;
        border: 1px solid rgba(34, 197, 94, 0.35);
    }

    .badge-pending {
        background: rgba(245, 158, 11, 0.15);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.35);
    }

    .badge-rejected {
        background: rgba(239, 68, 68, 0.15);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.35);
    }

    /* Pending Screen Notice Box */
    .pending-notice-box {
        background: rgba(30, 41, 59, 0.85);
        border: 1px solid rgba(245, 158, 11, 0.4);
        border-radius: 18px;
        padding: 2.2rem;
        margin: 2rem auto;
        max-width: 680px;
        text-align: center;
        box-shadow: 0 10px 35px rgba(245, 158, 11, 0.12);
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

    /* Code Snippet / Mono */
    .mono-code {
        font-family: 'JetBrains Mono', monospace;
        background: rgba(15, 23, 42, 0.7);
        padding: 0.18rem 0.45rem;
        border-radius: 6px;
        border: 1px solid rgba(148, 163, 184, 0.2);
        color: #38bdf8;
        font-size: 0.85em;
    }

    /* Metric cards in inspection */
    .metric-card {
        background: rgba(30, 41, 59, 0.7);
        border-radius: 12px;
        padding: 1.1rem;
        border: 1px solid rgba(148, 163, 184, 0.15);
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

    /* Footer */
    .corebox-footer {
        text-align: center;
        padding: 3rem 0 1.5rem 0;
        color: #64748b;
        font-size: 0.88rem;
        letter-spacing: 0.05em;
        border-top: 1px solid rgba(148, 163, 184, 0.1);
        margin-top: 3.5rem;
    }
    </style>
    """
