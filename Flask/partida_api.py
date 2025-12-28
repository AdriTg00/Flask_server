from flask import Blueprint, request, jsonify
from datetime import datetime
from firebase_admin import firestore

from .firebase_init import db  # 🔑 IMPORT RELATIVO

partidas_api = Blueprint("partidas_api", __name__)

@partidas_api.post("/partidas/guardar")
def guardar_partida():
    data = request.json

    jugador_id = data.get("jugador_id")
    if not jugador_id:
        return jsonify({"error": "jugador_id requerido"}), 400

    data["fecha"] = datetime.now()

    partida = {
        "nivel": data.get("nivel", 1),
        "tiempo": data.get("tiempo", 0),
        "puntuacion": data.get("puntuacion", 0),
        "muertes_nivel": data.get("muertes_nivel", 0),
        "pos_x": data.get("pos_x", 0),
        "pos_y": data.get("pos_y", 0),
        "fecha": data["fecha"]
    }

    ref = (
        db.collection("jugadores")
        .document(jugador_id)
        .collection("partidas")
        .add(partida)
    )

    return jsonify({
        "ok": True,
        "id": ref[1].id
    })


@partidas_api.get("/partidas/obtener")
def obtener_partidas():
    jugador_id = request.args.get("jugador")

    if not jugador_id:
        return jsonify({"error": "jugador requerido"}), 400

    partidas_ref = (
        db.collection("jugadores")
        .document(jugador_id)
        .collection("partidas")
        .order_by("fecha", direction=firestore.Query.DESCENDING)
    )

    resultado = []
    for doc in partidas_ref.stream():
        data = doc.to_dict()
        data["id"] = doc.id
        resultado.append(data)

    return jsonify(resultado), 200
