from flask import Flask
from .jugador_api import jugador_api
from .partida_api import partidas_api

app = Flask(__name__)

# Registrar rutas
app.register_blueprint(jugador_api)
app.register_blueprint(partidas_api)

@app.get("/")
def home():
    return "API funcionando correctamente"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
