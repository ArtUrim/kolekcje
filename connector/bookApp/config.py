import os

class Config:
    DB_CONFIG = {
        "user": os.getenv("DB_USER", "example"),
        "password": os.getenv("DB_PASSWORD", "example"),
        "host": os.getenv("DB_HOST", "db"),
        "port": int(os.getenv("DB_PORT", 3306)),
        "database": os.getenv("DB_NAME", "katalog")
    }
    SHARED_DIR = os.getenv("SHARED_DIR", "/app/shared")