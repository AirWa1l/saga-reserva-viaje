from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

LYRICS_URL = "http://lyrics-service:5001"
COMPOSITION_URL = "http://composition-service:5002" 
CAR_URL = "http://car-service:5003"
DELETE_URL = "http://delete-service:5006"

@app.route('/music', methods=['POST'])
def book_trip():
    user = request.json.get('user')
    successful_steps = []

    try:
        # Crear letra
        res = requests.post(f"{LYRICS_URL}/write", json={"user": user})
        if res.status_code != 200:
            raise Exception("Error en la creación de letra")
        successful_steps.append("lyrics")

        # Componer música
        res = requests.post(f"{COMPOSITION_URL}/reserve", json={"user": user})
        if res.status_code != 200:
            raise Exception("Error en composición musical")
        successful_steps.append("composition")

        # Reservar carro
        res = requests.post(f"{CAR_URL}/reserve", json={"user": user})
        if res.status_code != 200:
            raise Exception("Error en carro")
        successful_steps.append("car")

        # Eliminar canción 
        res = requests.post(f"{DELETE_URL}/delete", json={"user": user})
        if res.status_code != 200:
            raise Exception("Error en eliminación de canción")
        successful_steps.append("delete")

        return jsonify({"message": f"Canción completada para {user}"}), 200

    except Exception as e:
        print(f"❌ Error: {e}")
        # Compensar pasos exitosos
        if "car" in successful_steps:
            requests.post(f"{CAR_URL}/cancel", json={"user": user})
        if "composition" in successful_steps:
            requests.post(f"{COMPOSITION_URL}/cancel", json={"user": user})
        if "lyrics" in successful_steps:
            requests.post(f"{LYRICS_URL}/erase", json={"user": user})
        if "delete" in successful_steps:
            requests.post(f"{DELETE_URL}/delete", json={"user": user})
        return jsonify({"message": f"Error en la creación de canción para {user}. Se ejecutaron compensaciones."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
