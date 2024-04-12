import json
import os
import subprocess
from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId
import paho.mqtt.publish as publish
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

app.secret_key = 'myawesomesecretkey'

app.config['MONGO_URI'] = 'mongodb://localhost:27017/digitaltwin'
mongo = PyMongo(app)

process3d = None
process2d = None


@app.route('/api')
def api():
    return jsonify({'data': 'Hello, World!'})


@app.route('/users', methods=['POST'])
def create_user():
    # Receiving Data
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    if username and email and password:
        hashed_password = generate_password_hash(password)
        result = mongo.db.users.insert_one(
            {'username': username, 'email': email, 'password': hashed_password})
        response = jsonify({
            '_id': str(result.inserted_id),
            'username': username,
            'password': password,
            'email': email
        })
        response.status_code = 201
        return response
    else:
        return not_found()


@app.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.users.find()
    response = json_util.dumps(users)
    return Response(response, mimetype="application/json")


@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    print(id)
    user = mongo.db.users.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(user)
    return Response(response, mimetype="application/json")


@app.route('/api/login', methods=['POST'])
def login():
    # Receiving Data
    email = request.json['email']
    password = request.json['password']

    # Find the user by email
    user = mongo.db.users.find_one({'email': email})

    # If user not found, return error
    if not user:
        return jsonify({'message': 'User not found'}), 404

    # Check if the password is correct
    if not check_password_hash(user['password'], password):
        return jsonify({'message': 'Incorrect password'}), 401

    # If everything is correct, return a success message
    # In a real application, you would also return a token or session ID here
    return jsonify({'message': 'Login successful', 'username': user['username']}), 200


@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.users.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'User' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response


@app.route('/users/<_id>', methods=['PUT'])
def update_user(_id):
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    if username and email and password and _id:
        hashed_password = generate_password_hash(password)
        mongo.db.users.update_one(
            {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
            {'$set': {'username': username, 'email': email, 'password': hashed_password}})
        response = jsonify({'message': 'User' + _id + 'Updated Successfuly'})
        response.status_code = 200
        return response
    else:
        return not_found()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message': 'Resource Not Found ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response


@app.route('/api/run3D', methods=['POST'])
def run_3D():
    try:
        global process3d
        process3d = subprocess.Popen(["python3", "../Adapters/co_simulation/simulation_3D.py"])
        return jsonify({'message': 'Comando executado com sucesso'}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({'error': e}), 500


@app.route('/api/run2D', methods=['POST'])
def run_2D():
    try:
        global process2d
        process2d = subprocess.Popen(["python3", "../Adapters/co_simulation/simulation_2D.py"])
        return jsonify({'message': 'Comando iniciado com sucesso'}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({'error': e}), 500


@app.route('/api/addRandomTraffic', methods=['POST'])
def add_random_traffic():
    qtd = request.args.get('qtd')
    if qtd is None:
        return jsonify({'error': 'Parâmetro "qtd" é obrigatório na URL'}), 400

    try:
        publish.single("/addRandomTraffic", payload=f'{qtd}', hostname="localhost", port=1883)
        return jsonify({'message': f'Tráfego aleatório adicionado para {qtd} veículos'}), 200
    except Exception as e:
        return jsonify({'error': e}), 500

    # curl -X POST -d "" "http://localhost:5000/api/addRandomTraffic?qtd=500"


@app.route('/api/testaddRealCar', methods=['POST'])
def test_add_real_car():
    try:
        data = request.json  # Acessa o JSON enviado no corpo da solicitação
        # Aqui você pode manipular os dados como desejar
        print("Dados recebidos:", data)

        # Exemplo: extrair o ID do veículo do JSON recebido
        vehicle_id = data.get('objectID')
        if vehicle_id is not None:
            # Faça algo com o ID do veículo, como publicá-lo em um tópico MQTT
            publish.single("/realDatateste", payload=json.dumps(data), hostname="localhost", port=1883)

        return jsonify({'message': 'Veículo adicionado com sucesso'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # curl - X POST - H "Content-Type: application/json" -d '{
    #"acceleration": 0.0,
    #"classification": 5,
    #"cloudPersist": false,
    #"confidence": 100,
    #"heading": -25.311,
    #"latitude": 40.635327506990194,
    #"length": 5.6000000000000005,
    #"longitude": -8.660106693274248,
    #"objectID": 1015,
    #"receiverID": 1,
    #"speed": 10.9,
    #"test": {},
    #"timestamp": 1710954013.329629 }'   http://localhost:5000/api/testaddRealCar


@app.route('/api/addSimulatedCar', methods=['POST'])
def add_car():
    try:
        data = request.json  # Acessa o JSON enviado no corpo da solicitação
        # Aqui você pode manipular os dados como desejar
        print("Dados recebidos:", data)
        publish.single("/addSimulatedCar", payload=json.dumps(data), hostname="localhost", port=1883)
        return jsonify({'message': 'Veículo adicionado com sucesso'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    #curl - X POST - H "Content-Type: application/json" -d '{
    #"end": {"log": "-8.655386132941464", "lat": "40.63525392116133"},
    #"start": {"log": "-8.660106693274248", "lat": "40.635327506990194"}
    #}' http://localhost:5000/api/addSimulatedCar


@app.route('/api/endSimulation', methods=['POST'])
def end_simulation():
    try:
        publish.single("/endSimulation", payload="", hostname="localhost", port=1883)
        if process2d is not None:
            process2d.kill()

        if process3d is not None:
            process3d.kill()

        return jsonify({'message': 'Simulação finalizada com sucesso'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # curl -X POST -d "" "http://localhost:5000/api/endSimulation"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
