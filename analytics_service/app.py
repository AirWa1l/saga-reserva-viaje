from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/get', methods=['GET'])
def count_lyrics():
    try:
        # Kubernetes resuelve el nombre del servicio automáticamente
        response = requests.get("http://lyrics-service:5001/lyrics")
        if response.status_code == 200:
            liricas = response.json()
            cantidad = len(liricas)
            mensaje = f"La cantidad de canciones que se tienen son {cantidad}"
            return jsonify({"message": mensaje}), 200
        else:
            return jsonify({"error": "No se pudieron obtener las letras"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/roll', methods=['GET'])
def amount_delete_songs():
    try:
        response = requests.get("http://lyrics-service:5001/contador_borradas")
        if response.status_code == 200:
            return response.json(), 200
        else:
            return jsonify({"error": "No se pudo obtener el contador"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
