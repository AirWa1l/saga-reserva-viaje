from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

LYRICS_URL = "http://lyrics-service:5001"
COMPOSITION_URL = "http://composition-service:5002" 
ANALYTICS_URL = "http://analytics-service:5003"
DELETE_URL = "http://delete-service:5006"
DIGITAL_DELIVERY_URL = "http://digital-delivery-service:5009"
MASTERING_URL = "http://mastering-service:5010"
VOCAL_RECORDING_URL = "http://vocal-recording-service:5005"
MIXING_SERVICE_URL = "http://mixing-service:5007"

EMOTIONAL_REFUND_URL = "http://emotional-refund-service:5004"
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

        # Entrega digital
        res = requests.post(f"{DIGITAL_DELIVERY_URL}/deliver", json={"user": user})
        if res.status_code != 200:
            raise Exception("Error al entregar la cancion")
        successful_steps.append("digital_relivery")

        res = requests.post(f"{MASTERING_URL}/write", json={"user": user})
        if res.status_code != 200:
            raise Exception("Error al masterizar el track mezclado")
        successful_steps.append("mastering")

        # Grabar voz
        res = requests.post(f"{VOCAL_RECORDING_URL}/record", json={"user": user})
        if res.status_code != 200:
            raise Exception("Error al grabar la voz")
        successful_steps.append("vocal_recording")

        # Mezcla de sonido
        res = requests.post(f"{MIXING_SERVICE_URL}/record", json={"user": user})
        if res.status_code != 200:
            raise Exception("Error al grabar la voz")
        successful_steps.append("vocal_recording")
        res = requests.post(f"{EMOTIONAL_REFUND_URL}/write", json={"user": user}) 
        if res.status_code != 200:
            raise Exception("Error en el reembolso emocional")
        successful_steps.append("emotional_refund")

        # Obtener inspiración
        res = requests.post(f"{INSPIRATION_URL}/reserve", json={"user": user})
        if res.status_code != 200:
            raise Exception("Obtener inspiración fallida")
        successful_steps.append("inspiration") 

        return jsonify({"message": f"Obtenido las grabaciones de {user}"}), 200
        

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
        if "vocal_recording" in successful_steps:
            requests.post(f"{VOCAL_RECORDING_URL}/cancel", json={"user": user})
        if "mixing" in successful_steps:
            requests.post(f"{MIXING_SERVICE_URL}/cancel", json={"user": user})
        

        if "mastering" in successful_steps:
            requests.post(f"{MASTERING_URL}/cancel", json={"user": user})
        if "emotional_refund" in successful_steps:
            requests.post(f"{EMOTIONAL_REFUND_URL}/erase", json={"user": user})
        if "inspiration" in successful_steps:
            requests.post(f"{INSPIRATION_URL}/cancel", json={"user": user})
        return jsonify({"message": f"Revision de letras borradas de {user}."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
