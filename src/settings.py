import os


class Settings:
    PROJECT_NAME = "DNS Lookup API"
    VERSION = "0.1.0"
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", 5432)
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
    DB_NAME = os.getenv("DB_NAME", "app_db")


settings = Settings()
