import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
# 🔐 JWT CONFIG
    JWT_REFRESH_COOKIE_NAME = "refresh_token"
    JWT_TOKEN_LOCATION = ["headers", "cookies"]  # accepte les 2
    JWT_COOKIE_SECURE = False  # True si HTTPS
    JWT_ACCESS_COOKIE_PATH = "/"
    JWT_REFRESH_COOKIE_PATH = "/auth/refresh"
    JWT_COOKIE_CSRF_PROTECT = False  # désactive la protection CSRF pour test local
