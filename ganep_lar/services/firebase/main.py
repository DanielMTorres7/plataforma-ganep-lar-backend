import firebase_admin
from firebase_admin import credentials

# Caminho para o arquivo de credenciais
cred_path = 'ganep_lar/services/firebase/firebase-credentials.json'

# Inicialize o Firebase Admin SDK
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)