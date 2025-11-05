from flask import Flask, request, jsonify

app = Flask(__name__)

LYRICS_URL = "http://lyrics-service:5001"

# Helper: obtener letras desde lyrics_service
def fetch_lyrics(user):
    """
    Intenta traer las letras asociadas a 'user' desde lyrics_service.
    Se asume un endpoint GET /get?user=<user> en lyrics_service. Ajustar si difiere.
    Devuelve el JSON retornado por lyrics_service o lanza Exception en fallo.
    """
    try:
        res = requests.get(f"{LYRICS_URL}/get", params={"user": user}, timeout=5)
    except requests.RequestException as e:
        raise Exception(f"No se pudo conectar a lyrics_service: {e}")
    if res.status_code != 200:
        raise Exception(f"lyrics_service respondió {res.status_code}")
    return res.json()

# Helper: procesar letras para generar métricas simples
def compute_statistics(lyrics_payload):
    """
    Espera un dict con clave 'lyrics' (texto).
    Retorna estadísticas simples (palabras, caracteres, palabras únicas).
    """
    text = lyrics_payload.get("lyrics", "") if isinstance(lyrics_payload, dict) else ""
    words = text.split()
    return {
        "word_count": len(words),
        "char_count": len(text),
        "unique_words": len(set(words))
    }

# Endpoint que el orquestador invoca para "get" analytics
@app.route('/get', methods=['POST'])
def get():
    """
    Endpoint invocado por el orquestador con:
    POST {ANALYTICS_URL}/get json={"user": user}
    Esta función:
    - trae las letras con fetch_lyrics(user)
    - computa estadísticas con compute_statistics(...)
    - simula almacenar/registrar analytics y responde 200 con las métricas
    """
    user = request.json.get("user")
    if not user:
        return jsonify({"error": "user requerido"}), 400
    try:
        lyrics_data = fetch_lyrics(user)
        stats = compute_statistics(lyrics_data)
        # Aquí se podría persistir las stats en una BD, enviar a otro servicio, etc.
        return jsonify({"message": "Analytics reservada", "user": user, "stats": stats}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint que el orquestador invoca para "roll" analytics
@app.route('/roll', methods=['POST'])
def roll():
    """
    Endpoint invocado por el orquestador con:
    POST {ANALYTICS_URL}/roll json={"user": user}
    Esta función realiza la compensación (borrado/rollback) de analytics para el user.
    """
    user = request.json.get("user")
    if not user:
        return jsonify({"error": "user requerido"}), 400
    # Simular eliminación/compensación de analytics
    # Si se tuviera una BD, aquí se eliminarían los registros asociados al user.
    return jsonify({"message": f"Analytics rollada para {user}"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
