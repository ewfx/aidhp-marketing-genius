import firebase_admin
from config import Config
from firebase_admin import credentials, firestore

FIREBASE_CREDENTIALS = Config.FIREBASE_SERVICE_ACCOUNT_FILE
print(FIREBASE_CREDENTIALS)

def init_db():
    cred = credentials.Certificate(FIREBASE_CREDENTIALS)
    firebase_admin.initialize_app(cred)
    print(f"Firebase project ID: {firebase_admin.get_app().project_id}")

    return firestore.client()
