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
