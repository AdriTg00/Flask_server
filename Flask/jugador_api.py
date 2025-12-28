from flask import Blueprint, request, jsonify
from firebase_init import db
from datetime import datetime
from uuid import uuid4

jugador_api = Blueprint("jugador_api", __name__)

# ===============================
# VALIDAR JUGADOR
# ===============================
@jugador_api.post("/jugadores/validar")
def validar_jugador():
    data = request.json
    nombre = data.get("nombre")

    if not nombre:
        return jsonify({"error": "Nombre requerido"}), 400

    query = db.collection("jugadores").where("nombre", "==", nombre).stream()
    existe = any(query)

    return jsonify({"existe": existe}), 200


# ===============================
# CREAR JUGADOR
# ===============================
@jugador_api.post("/jugadores/crear")
def crear_jugador():
    data = request.json
    nombre = data.get("nombre")

    if not nombre:
        return jsonify({"error": "Nombre requerido"}), 400

    jugador_id = uuid4().hex

    db.collection("jugadores").document(jugador_id).set({
        "nombre": nombre,
        "fecha_creacion": datetime.now(),
        "tiempo_total": 0,
        "puntuacion_total": 0,
        "niveles_superados": 0
    })

    return jsonify({
        "id": jugador_id,
        "nombre": nombre
    }), 200


# ===============================
# ACTUALIZAR ESTADÍSTICAS
# ===============================
@jugador_api.post("/jugadores/estadisticas")
def actualizar_estadisticas():
    data = request.json
    jugador_id = data.get("jugador_id")

    if not jugador_id:
        return jsonify({"error": "jugador_id requerido"}), 400

    ref = db.collection("jugadores").document(jugador_id)
    doc = ref.get()

    if not doc.exists:
        return jsonify({
            "error": "Jugador no existe",
            "jugador_id": jugador_id
        }), 404

    ref.set({
        "tiempo_total": float(data.get("tiempo_total", 0)),
        "puntuacion_total": int(data.get("puntuacion_total", 0)),
        "niveles_superados": int(data.get("niveles_superados", 0)),
        "ultima_actualizacion": datetime.now()
    }, merge=True)

    return jsonify({"ok": True}), 200
