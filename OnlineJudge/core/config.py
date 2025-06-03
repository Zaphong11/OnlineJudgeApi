from dotenv import load_dotenv
import os

"""Configuration settings for the application."""

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    REDIS_URL: str = os.getenv("REDIS_URL")

settings = Settings()