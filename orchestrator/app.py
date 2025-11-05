from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

LYRICS_URL = "http://lyrics-service:5001"
HOTEL_URL = "http://hotel-service:5002"
CAR_URL = "http://car-service:5003"
INSPIRATION_URL = "http://inspiration-service:5008"

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

        # Reservar hotel
        res = requests.post(f"{HOTEL_URL}/reserve", json={"user": user})
        if res.status_code != 200:
            raise Exception("Error en hotel")
        successful_steps.append("hotel")

        # Reservar carro
        res = requests.post(f"{CAR_URL}/reserve", json={"user": user})
        if res.status_code != 200:
            raise Exception("Error en carro")
        successful_steps.append("car")

        # Obtener inspiración
        res = requests.post(f"{INSPIRATION_URL}/reserve", json={"user": user})
        if res.status_code != 200:
            raise Exception("Obtener inspiración fallida")
        successful_steps.append("inspiration")

        return jsonify({"message": f"Reserva completada para {user}"}), 200

    except Exception as e:
        print(f"❌ Error: {e}")
        # Compensar pasos exitosos
        if "car" in successful_steps:
            requests.post(f"{CAR_URL}/cancel", json={"user": user})
        if "hotel" in successful_steps:
            requests.post(f"{HOTEL_URL}/cancel", json={"user": user})
        if "lyrics" in successful_steps:
            requests.post(f"{LYRICS_URL}/erase", json={"user": user})
        if "inspiration" in successful_steps:
            requests.post(f"{INSPIRATION_URL}/cancel", json={"user": user})
        return jsonify({"message": f"Error en la reserva para {user}. Se ejecutaron compensaciones."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
