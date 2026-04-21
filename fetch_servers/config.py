import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_KEY = os.getenv("API_KEY")
    JWT_SECRET = os.getenv("JWT_SECRET")
    SECRET_KEY = os.getenv("SECRET_KEY")
    RATE_LIMIT = '50 per minute'

