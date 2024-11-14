import os
import sys
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

PYTEST = "pytest" in sys.argv[0] or sys.argv[0] == "-c"
env_path = BASE_DIR / "test.env" if PYTEST else BASE_DIR / ".env"

load_dotenv(env_path)

MAT_HOST = os.environ.get("MAT_HOST", "localhost")
MAT_PORT = os.environ.get("MAT_PORT", 8095)
MAT_SECURE = os.environ.get("MAT_SECURE", False)
