from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

LYRICS_URL = "http://lyrics-service:5001"
<<<<<<< HEAD
HOTEL_URL = "http://hotel-service:5002"
CAR_URL = "http://car-service:5003"
VOCAL_RECORDING_URL = "http://vocal-recording-service:5005"
=======
COMPOSITION_URL = "http://composition-service:5002" 
ANALYTICS_URL = "http://analytics-service:5003"
DELETE_URL = "http://delete-service:5006"
DIGITAL_DELIVERY_URL = "http://digital-delivery-service:5009"
>>>>>>> develop

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

        #Analytics
        res = requests.post(f"{ANALYTICS_URL}/get", json={"user": user})
        if res.status_code != 200:
            raise Exception("Error en analiticas :()")
        successful_steps.append("analytics")

        # eliminar cancion
        res = requests.post(f"{DELETE_URL}/delete", json={"user": user})
        if res.status_code != 200:
            raise Exception("Error al borrar la cancion")
        successful_steps.append("delete")

        res = requests.post(f"{DIGITAL_DELIVERY_URL}/deliver", json={"user": user})
        if res.status_code != 200:
            raise Exception("Error al entregar la cancion")
        successful_steps.append("digital_relivery")

        return jsonify({"message": f"Obtenido las letras de {user}"}), 200
        

    except Exception as e:
        print(f"❌ Error: {e}")
        # Compensar pasos exitosos
        if "composition" in successful_steps:
            requests.post(f"{COMPOSITION_URL}/cancel", json={"user": user})
        if "lyrics" in successful_steps:
            requests.post(f"{LYRICS_URL}/erase", json={"user": user})
        if "analytics" in successful_steps:
            requests.post(f"{ANALYTICS_URL}/roll", json={"user": user})
        if "delete" in successful_steps:
            requests.post(f"{DELETE_URL}/cancel", json={"user": user})
        if "digital_delivery" in successful_steps:
            requests.post(f"{DIGITAL_DELIVERY_URL}/cancel", json={"user": user})
        return jsonify({"message": f"Revision de letras borradas de {user}."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
