from flask import Flask, request, jsonify

app = Flask(__name__)

liricas = []

@app.route('/write', methods=['POST'])
def escribir_cancion():
    data = request.json
    user = data.get('user')
    mood = data.get('mood')
    theme = data.get('theme')
    lyrics = data.get('lyrics')

    lirica = {
        "user": user,
        "mood": mood,
        "theme": theme,
        "lyrics": lyrics
    }
    liricas.append(lirica)
    return jsonify({"message": f"Letra creada para {user}", "data": lirica}), 200

@app.route('/erase', methods=['POST'])

def borrar_letra():
    data = request.json
    user = data.get('user')

    for lirica in liricas:
        if lirica['user'] == user:
            liricas.remove(lirica)
            return jsonify({"message": f"Letra eliminada para {user}"}),200

    return jsonify({"message": "Letra no encontrada"}), 404

@app.route('/lyrics', methods=['GET'])
def ver_liricas():
    return jsonify(liricas), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)