from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import json
import os

app = Flask(__name__)


# ======================================================
#              🔥 INICIALIZAR FIREBASE 🔥
# ======================================================

firebase_key = os.getenv("FIREBASE_KEY")

if not firebase_key:
    raise Exception("ERROR: No se encontró la variable de entorno FIREBASE_KEY")

cred_dict = json.loads(firebase_key)
cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred)

db = firestore.client()


# ======================================================
#                 🟦   JUGADORES   🟦
# ======================================================

@app.route("/jugadores/validar", methods=["POST"])
def validar_jugador():
    """Devuelve {existe: True/False}"""
    data = request.json
    nombre = data.get("nombre")

    if not nombre:
        return jsonify({"error": "Nombre requerido"}), 400

    doc = db.collection("jugadores").document(nombre).get()

    return jsonify({"existe": doc.exists}), 200


@app.route("/jugadores/crear", methods=["POST"])
def crear_jugador():
    """Crea un jugador si no existe."""
    data = request.json
    nombre = data.get("nombre")

    if not nombre:
        return jsonify({"error": "Nombre requerido"}), 400

    doc_ref = db.collection("jugadores").document(nombre)
    doc = doc_ref.get()

    if doc.exists:
        return jsonify({"creado": False, "error": "Jugador ya existe"}), 200

    doc_ref.set({
        "nombre": nombre,
        "fecha_creacion": datetime.now(),
    })

    return jsonify({"creado": True}), 200


@app.route("/jugadores/obtener", methods=["GET"])
def obtener_jugador():
    """Devuelve datos del jugador."""
    nombre = request.args.get("nombre")

    if not nombre:
        return jsonify({"error": "Nombre requerido"}), 400

    doc = db.collection("jugadores").document(nombre).get()

    if not doc.exists:
        return jsonify({"error": "No existe"}), 404

    return jsonify(doc.to_dict()), 200


# ======================================================
#                 🟨   PARTIDAS   🟨
# ======================================================

@app.route("/partidas/guardar", methods=["POST"])
def guardar_partida():
    """Guarda una nueva partida."""
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
    """Devuelve todas las partidas de un jugador."""
    jugador = request.args.get("jugador")

    if not jugador:
        return jsonify({"error": "Jugador requerido"}), 400

    partidas = db.collection("partidas") \
        .where("jugador_id", "==", jugador) \
        .stream()

    resultado = []

    for p in partidas:
        data = p.to_dict()
        data["id"] = p.id
        resultado.append(data)

    return jsonify(resultado), 200


# ======================
# LOCALHOST (solo pruebas)
# ======================
if __name__ == "__main__":
    app.run(port=5000)
