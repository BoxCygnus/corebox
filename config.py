import os
from dotenv import load_dotenv

# Load environment variables from .env file if available
load_dotenv()

# Application Settings
APP_NAME = "COREBOX"
APP_SUBTITLE = "Your project management, minus the manual hassle."
APP_DESCRIPTION = "Data storage, automated inspection, and other supportive tools."
APP_FOOTER = "Developed by Box"

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
