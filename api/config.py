import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    MONGO_URI = os.environ.get('MONGO_URI')
    MONGO_DBNAME = 'ballet_motion'
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'uploads')
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or "jwt_secret_key"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    BASE_URL = 'http://localhost:5000'
    OTP_EXPIRY_MINUTES = 10


class ProductionConfig(Config):
    BASE_URL = 'https://yourproductiondomain.com'

class DevelopmentConfig(Config):
    DEBUG = True
