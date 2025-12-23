from flask import Blueprint, request, jsonify
from firebase_init import db
from datetime import datetime

partidas_api = Blueprint("partidas_api", __name__)

@partidas_api.get("/jugadores/<nombre>/partidas")
def obtener_partidas(nombre):
    partidas = []
    docs = db.collection("jugadores").document(nombre).collection("partidas").stream()
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        partidas.append(data)
    return jsonify(partidas)

@partidas_api.post("/jugadores/<nombre>/partidas")
def guardar_partida(nombre):
    data = request.json
    data["fecha"] = datetime.now()

    ref = (
        db.collection("jugadores")
        .document(nombre)
        .collection("partidas")
        .document()   # ← ID automático, pero controlado
    )

    ref.set(data)

    return jsonify({
        "ok": True,
        "id": ref.id
    })

@partidas_api.delete("/jugadores/<nombre>/partidas/<id>")
def borrar_partida(nombre, id):
    db.collection("jugadores").document(nombre).collection("partidas").document(id).delete()
    return jsonify({"ok": True})
