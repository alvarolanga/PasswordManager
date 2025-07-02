import os

class Config:
    # Use a constant secret key for sessions (you can load from env too)
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-dev-flask-secret')

    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    ENCRYPTION_KEY = os.environ.get(
        'ENCRYPTION_KEY',
        'FX1hGf90JSNfVnHLdghBDJUzTy8ZgE6HdR-GR6xW_1Q='
    )
