from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Almacenamos las disculpas en memoria
apologies = []

# 1️⃣ Función para recibir letras desde el lyrics_service
@app.route('/receive_lyrics', methods=['GET'])
def receive_lyrics():
    try:
        # Suponemos que el lyrics_service corre en el puerto 5001
        response = requests.get("http://lyrics_service:5001/lyrics")
        if response.status_code == 200:
            lyrics_data = response.json()
            return jsonify({"message": "Letras recibidas exitosamente", "data": lyrics_data}), 200
        else:
            return jsonify({"error": "No se pudieron obtener las letras"}), response.status_code
    except Exception as e:
        return jsonify({"error": f"Error al conectar con lyrics_service: {str(e)}"}), 500


# 2️⃣ Función para publicar una disculpa (reembolso emocional)
@app.route('/post_apology', methods=['POST'])
def post_apology():
    data = request.json
    user = data.get('user')
    reason = data.get('reason', 'Lo sentimos, la canción no cumplió tus expectativas.')

    if not user:
        return jsonify({"error": "Debe especificarse un usuario"}), 400

    apology = {
        "user": user,
        "apology": f"Querido {user}, lamentamos mucho que la letra no haya tocado tu corazón. {reason}"
    }

    apologies.append(apology)
    return jsonify({"message": "Disculpa creada", "data": apology}), 200


# 3️⃣ Función para borrar una disculpa
@app.route('/erase', methods=['POST'])
def erase_apology():
    data = request.json
    user = data.get('user')

    if not user:
        return jsonify({"error": "Debe especificarse un usuario"}), 400

    for apology in apologies:
        if apology['user'] == user:
            apologies.remove(apology)
            return jsonify({"message": f"Disculpa eliminada para {user}"}), 200

    return jsonify({"message": "Disculpa no encontrada"}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)

