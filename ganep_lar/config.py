from dotenv import load_dotenv
load_dotenv()

from os import getenv


# Chave secreta para assinar o JWT
SECRET_KEY = getenv("SECRET_KEY")

# URL de login do Firebase
FIREBASE_API_KEY = getenv('FIREBASE_API_KEY')
FIREBASE_LOGIN_URL = f'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}'


__all__ = [
    'SECRET_KEY',
    'FIREBASE_API_KEY',
    'FIREBASE_LOGIN_URL'
]