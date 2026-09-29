import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# Application Settings
APP_NAME = "COREBOX"
APP_SUBTITLE = "Đơn giản hóa hành trình chuyển đổi số của bạn"
APP_DESCRIPTION = "Lưu trữ dữ liệu, kiểm tra tự động và các công cụ hỗ trợ."
APP_FOOTER = "Phát triển bởi Box"

# Admin Configuration
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "happyclone96@gmail.com").strip().lower()

# Cloudflare Configuration
CLOUDFLARE_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID", "").strip()
CLOUDFLARE_D1_DATABASE_ID = os.getenv("CLOUDFLARE_D1_DATABASE_ID", "").strip()
CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN", "").strip()

# Local SQLite Database Path (used when Cloudflare D1 credentials are not set)
DB_PATH = os.getenv("DB_PATH", os.path.join(os.path.dirname(__file__), "data", "corebox.db"))

# Secret Key for session / security
SECRET_KEY = os.getenv("SECRET_KEY", "corebox-secret-key-super-safe-2026")
