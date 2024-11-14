import os
import sys
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

PYTEST = "pytest" in sys.argv[0] or sys.argv[0] == "-c"
env_path = BASE_DIR / "test.env" if PYTEST else BASE_DIR / ".env"

load_dotenv(env_path)

DEBUG = os.getenv("DEBUG", "False") == "True"

MAT_HOST = os.getenv("MAT_HOST", "localhost")
MAT_PORT = int(os.getenv("MAT_PORT", "8095"))
MAT_SECURE = os.getenv("MAT_SECURE", "False") == "True"
