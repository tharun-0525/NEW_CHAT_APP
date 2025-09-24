import os
from dotenv import load_dotenv

load_dotenv("app/.env")

DATABASE_URL = os.getenv("DATABASE_URL")
# App settings
DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1")
