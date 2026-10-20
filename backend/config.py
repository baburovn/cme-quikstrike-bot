import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# Telegram Bot
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://bbrv.ru")

# CME Credentials (from cme_credentials.py or .env)
try:
    try:
        from backend import cme_credentials
    except ImportError:
        import cme_credentials
    CME_LOGIN = getattr(cme_credentials, "CME_LOGIN", os.getenv("CME_LOGIN", ""))
    CME_PASSWORD = getattr(cme_credentials, "CME_PASSWORD", os.getenv("CME_PASSWORD", ""))
except Exception:
    CME_LOGIN = os.getenv("CME_LOGIN", "")
    CME_PASSWORD = os.getenv("CME_PASSWORD", "")

# Server / API
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8080"))
UPDATE_INTERVAL_SECONDS = int(os.getenv("UPDATE_INTERVAL_SECONDS", "10"))
