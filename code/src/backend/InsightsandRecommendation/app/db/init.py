import firebase_admin
from config import Config
from firebase_admin import credentials, firestore

FIREBASE_CREDENTIALS = Config.FIREBASE_SERVICE_ACCOUNT_FILE

def init_db():
    cred = credentials.Certificate(FIREBASE_CREDENTIALS)
    firebase_admin.initialize_app(cred)

    return firestore.client()
