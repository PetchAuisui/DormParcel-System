import os

class Config:
    secret_key = os.getenv("SECRET_KEY", "super-secret-key")

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    if not SQLALCHEMY_DATABASE_URI:
        raise  ValueError("DATABASE_URL environment variable not set")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    Debug = os.getenv("Flask_ENV") == "development"


