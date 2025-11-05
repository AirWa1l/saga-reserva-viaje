import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

voces = []

@app.route('/record', methods=['POST'])
def grabar_voz():
    data = request.json
    user = data.get('user')
    tone = data.get('tone')
    voice = data.get('voice')

    grabacion = {
        "user": user,
        "tone": tone,
        "voice": voice
    }
    voces.append(grabacion)
    return jsonify({"message": f"La voz fue grabada para {user}", "data": voces}), 200

@app.route('/cancel', methods=['POST'])
def borrar_grabacion():
    data = request.json
    user = data.get('user')

    for grabacion in voces:
        if grabacion['user'] == user:
            voces.remove(grabacion)
            return jsonify({"message": f"Grabación eliminada para {user}"}),200

    return jsonify({"message": "Grabación no encontrada"}), 404

@app.route('/voices', methods=['GET'])
def ver_grabaciones():
    return jsonify(voces), 200

@app.route('/get', methods=['GET'])
def lyrics_recorded():
    user = request.args.get('user')
    try:
        # Kubernetes resuelve el nombre del servicio automáticamente
        response = requests.get("http://lyrics-service:5001/lyrics")
        if response.status_code == 200:
            liricas = response.json()
            canciones = str(liricas)
            mensaje = f"Las canciones cantadas por el usuario {user}son: {canciones}"
            return jsonify({"message": mensaje}), 200
        else:
            return jsonify({"error": "No se pudieron obtener las canciones"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)

