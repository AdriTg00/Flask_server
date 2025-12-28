import firebase_admin
from firebase_admin import credentials, firestore
import json
import os

if not firebase_admin._apps:
    firebase_key = os.getenv("FIREBASE_KEY")
    if not firebase_key:
        raise Exception("ERROR: No se encontró FIREBASE_KEY")

    cred_dict = json.loads(firebase_key)
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()
