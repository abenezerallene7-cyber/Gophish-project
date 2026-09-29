import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-me'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///vulnscope.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # API keys (global fallbacks, can be overridden per user)
    VIRUSTOTAL_API_KEY = os.environ.get('VIRUSTOTAL_API_KEY', '')
    ABUSEIPDB_API_KEY = os.environ.get('ABUSEIPDB_API_KEY', '')
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
    WPSCAN_API_TOKEN = os.environ.get('WPSCAN_API_TOKEN', '')
    SHODAN_API_KEY = os.environ.get('SHODAN_API_KEY', '')

    # Celery
    CELERY_BROKER_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')