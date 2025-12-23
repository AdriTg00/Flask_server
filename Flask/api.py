from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import json
import os
from uuid import uuid4

app = Flask(__name__)

# ======================================================
#               INICIALIZAR FIREBASE 
# ======================================================

firebase_key = os.getenv("FIREBASE_KEY")

if not firebase_key:
    raise Exception("ERROR: No se encontró la variable de entorno FIREBASE_KEY")

cred_dict = json.loads(firebase_key)
cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred)

db = firestore.client()


# ======================================================
#                    JUGADORES   
# ======================================================

@app.route("/jugadores/validar", methods=["POST"])
def validar_jugador():
    data = request.json
    nombre = data.get("nombre")

    if not nombre:
        return jsonify({"error": "Nombre requerido"}), 400

    query = db.collection("jugadores").where("nombre", "==", nombre).stream()
    existe = any(query)

    return jsonify({"existe": existe}), 200


@app.route("/jugadores/crear", methods=["POST"])
def crear_jugador():
    data = request.json
    nombre = data.get("nombre")

    if not nombre:
        return jsonify({"error": "Nombre requerido"}), 400

    # Generar ID único
    user_id = uuid4().hex

    db.collection("jugadores").document(user_id).set({
        "nombre": nombre,
        "fecha_creacion": datetime.now()
    })

    return jsonify({
        "id": user_id,
        "nombre": nombre
    }), 200


@app.route("/jugadores/obtener", methods=["GET"])
def obtener_jugador():
    """Devuelve datos del jugador por nombre."""
    nombre = request.args.get("nombre")

    if not nombre:
        return jsonify({"error": "Nombre requerido"}), 400

    query = db.collection("jugadores").where("nombre", "==", nombre).stream()
    for doc in query:
        data = doc.to_dict()
        data["id"] = doc.id
        return jsonify(data), 200

    return jsonify({"error": "No existe"}), 404


# ======================================================
#                   PARTIDAS   
# ======================================================

@app.route("/partidas/guardar", methods=["POST"])
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


@app.route("/partidas/obtener", methods=["GET"])
def obtener_partidas():
    jugador_id = request.args.get("jugador")

    if not jugador_id:
        return jsonify({"error": "Jugador requerido"}), 400

    partidas = db.collection("partidas")\
        .where("jugador_id", "==", jugador_id).stream()

    resultado = []
    for p in partidas:
        data = p.to_dict()
        data["id"] = p.id
        resultado.append(data)

    return jsonify(resultado), 200


if __name__ == "__main__":
    app.run(port=5000)
