import os
import subprocess
from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId
import paho.mqtt.publish as publish
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

app.secret_key = 'myawesomesecretkey'

app.config['MONGO_URI'] = 'mongodb://localhost:27017/digitaltwin'
mongo = PyMongo(app)


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
        subprocess.run(["python3", "../Adapters/co_simulation/simulation_3D.py",
                        "Adapters/co_simulation/sumo_configuration/ruadapega.sumocfg", "--tls-manager", "carla",
                        "--sumo-gui"], check=True)
        return jsonify({'message': 'Comando executado com sucesso'}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({'error': e}), 500


@app.route('/api/run2D', methods=['POST'])
def run_2D():
    try:
        subprocess.Popen(["python3", "../Adapters/co_simulation/simulation_2D.py"])
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


if __name__ == '__main__':
    app.run(debug=True)
