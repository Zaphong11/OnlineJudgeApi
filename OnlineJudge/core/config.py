from dotenv import load_dotenv
import os

"""Configuration settings for the application."""

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")

settings = Settings()