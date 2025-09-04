import os

from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()


DB_URL = os.getenv(
    "DB_URL", "postgresql+psycopg2://taskhub:SuperSecret123@localhost:5432/taskhub"
)
# DB_URL = os.getenv("DB_URL", "postgresql+psycopg2://user:pass@localhost:5432/taskhub")

JWT_SECRET = os.getenv("JWT_SECRET", "dev_secret_key")
JWT_EXPIRE_DAYS = int(os.getenv("JWT_EXPIRE_DAYS", "7"))
JWT_ALG = "HS256"
