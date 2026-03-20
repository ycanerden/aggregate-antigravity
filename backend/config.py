import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(ENV_PATH)

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/aggregator.db")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# Playwright settings
HEADLESS_BROWSER = True
