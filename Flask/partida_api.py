from flask import Blueprint, request, jsonify
from firebase_init import db
from datetime import datetime

partidas_api = Blueprint("partidas_api", __name__)

@partidas_api.get("/partidas/<jugador_id>")
def obtener_partidas(jugador_id):
    docs = (
        db.collection("jugadores")
        .document(jugador_id)
        .collection("partidas")
        .stream()
    )

    partidas = []
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        partidas.append(data)

    return jsonify(partidas)



@partidas_api.post("/partidas/guardar")
def guardar_partida():
    data = request.json

    jugador_id = data.get("jugador_id")
    if not jugador_id:
        return jsonify({"error": "jugador_id requerido"}), 400

    data["fecha"] = datetime.now()

    ref = (
        db.collection("jugadores")
          .document(jugador_id)
          .collection("partidas")
          .add(data)
    )

    return jsonify({
        "ok": True,
        "id": ref[1].id
    })
