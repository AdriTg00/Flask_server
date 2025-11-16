from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# Inicializar Firebase
cred = credentials.Certificate("clave.json")  # <-- aquí va tu clave JSON de Firebase
firebase_admin.initialize_app(cred)

db = firestore.client()

app = Flask(__name__)

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


if __name__ == "__main__":
    app.run(port=5000)
