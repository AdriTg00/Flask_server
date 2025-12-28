from flask import Blueprint, request, jsonify
from datetime import datetime
from firebase_admin import firestore

from .firebase_init import db

partidas_api = Blueprint("partidas_api", __name__)

@partidas_api.post("/partidas/guardar")
def guardar_partida():
    data = request.json
    jugador_id = data.get("jugador_id")

    if not jugador_id:
        return jsonify({"error": "Jugador requerido"}), 400

    ref = (
        db.collection("jugadores")
        .document(jugador_id)
        .collection("partidas")
        .document()
    )

    ref.set({
        "nivel": data.get("nivel"),
        "tiempo": data.get("tiempo"),
        "puntuacion": data.get("puntuacion"),
        "muertes_nivel": data.get("muertes_nivel"),
        "fecha": datetime.now()
    })

    return jsonify({"ok": True, "id": ref.id}), 200


@partidas_api.get("/partidas/obtener")
def obtener_partidas():
    jugador_id = request.args.get("jugador")

    if not jugador_id:
        return jsonify({"error": "Jugador requerido"}), 400

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
