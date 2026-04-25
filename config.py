import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / os.getenv("DATA_DIR", "data")
EXPORTS_DIR = BASE_DIR / os.getenv("EXPORTS_DIR", "exports")

# Ensure directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Database
DB_PATH = os.getenv("DB_PATH", str(DATA_DIR / "smart_expense_analyzer.db"))

# Optional AI config
USE_LLM = os.getenv("USE_LLM", "false").lower() in ("true", "1", "yes")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-opus-20240229")

# App config
APP_ENV = os.getenv("APP_ENV", "development")
