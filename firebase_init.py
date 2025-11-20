import firebase_admin
from firebase_admin import credentials, firestore
import os

# Render guarda claves como variables de entorno
cred = credentials.Certificate("clave.json")

firebase_admin.initialize_app(cred)
db = firestore.client()
