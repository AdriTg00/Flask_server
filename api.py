from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import json
import os

app = Flask(__name__)

# ========================
#  Inicializar Firebase
# ========================

# Leemos la clave directamente desde la variable de entorno
firebase_key = os.getenv("FIREBASE_KEY")

if not firebase_key:
    raise Exception("ERROR: No se encontró la variable de entorno FIREBASE_KEY")

# Convertimos el texto del JSON a un diccionario
cred_dict = json.loads(firebase_key)

# Creamos las credenciales a partir del diccionario
cred = credentials.Certificate(cred_dict)

# Inicializamos Firebase
firebase_admin.initialize_app(cred)

# Cliente Firestore
db = firestore.client()

# ========================
#       ENDPOINTS
# ========================

@app.route("/guardar_partida", methods=["POST"])
def guardar_partida():
    data = request.json

    db.collection("partidas").add({
        "jugador_id": data.get("jugador_id"),
        "nivel": data.get("nivel"),
        "tiempo": data.get("tiempo"),
        "puntuacion": data.get("puntuacion"),
        "muertes_nivel": data.get("muertes_nivel"),
        "tipo": data.get("tipo"),
        "fecha": datetime.now()
    })

    return jsonify({"status": "ok"}), 200


# Render no usa esto, pero sirve para localhost
if __name__ == "__main__":
    app.run(port=5000)
