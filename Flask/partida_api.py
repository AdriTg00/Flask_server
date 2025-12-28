from flask import Blueprint, request, jsonify
from firebase_init import db
from datetime import datetime
from firebase_admin import firestore

partidas_api = Blueprint("partidas_api", __name__)

# ===============================
# GUARDAR PARTIDA
# ===============================
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
        "pos_x": data.get("pos_x"),
        "pos_y": data.get("pos_y"),
        "tipo": "guardado",
        "fecha": datetime.now()
    })

    return jsonify({
        "ok": True,
        "partida_id": ref.id
    }), 200


# ===============================
# OBTENER PARTIDAS
# ===============================
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
