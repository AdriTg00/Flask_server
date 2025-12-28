from flask import Blueprint, request, jsonify
from firebase_init import db

jugador_api = Blueprint("jugador_api", __name__)

@jugador_api.post("/jugadores/validar")
def validar_jugador():
    data = request.json
    nombre = data.get("nombre")
    
    doc = db.collection("jugadores").document(nombre).get()
    return jsonify({"existe": doc.exists})

@jugador_api.post("/jugadores/crear")
def crear_jugador():
    data = request.json
    nombre = data.get("nombre")

    db.collection("jugadores").document(nombre).set({"creado": True})
    return jsonify({"ok": True})

@jugador_api.post("/jugadores/estadisticas")
def actualizar_estadisticas():
    data = request.json

    jugador_id = data.get("jugador_id")
    if not jugador_id:
        return jsonify({"error": "jugador_id requerido"}), 400

    ref = db.collection("jugadores").document(jugador_id)

    # Comprobación explícita (muy útil para debug)
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





