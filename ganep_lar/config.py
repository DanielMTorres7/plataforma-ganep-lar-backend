import os
from dotenv import load_dotenv
load_dotenv()


class Config:
    FIREBASE_API_KEY = os.getenv('FIREBASE_API_KEY')
    FIREBASE_LOGIN_URL = f'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}'
    
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///users.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("SECRET_KEY")