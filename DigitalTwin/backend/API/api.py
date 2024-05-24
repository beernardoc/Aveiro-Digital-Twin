import os
import sys
import threading
from asyncio import sleep
import json
import subprocess
from flask import Flask, request, jsonify, Response, make_response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import requests
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import flask_socketio as socketio
from flask_swagger_ui import get_swaggerui_blueprint
from flask_jwt_extended import decode_token, JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import check_password_hash
from pymongo import MongoClient
from datetime import datetime

# # Adicione o diretório raiz do projeto ao PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Adapters.co_simulation.realdata.create_sumocfg import RealData

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = socketio.SocketIO(app, cors_allowed_origins="*")

app.secret_key = 'myawesomesecretkey'
app.config['JWT_SECRET_KEY'] = 'mysecretkey'

# app.config['MONGO_URI'] = 'mongodb://localhost:27017/digitaltwin'
# mongo = PyMongo(app)
mongo_client = MongoClient(host='localhost', port=27017, username='admin', password='password')
mongo = mongo_client['digitaltwin']
jwt = JWTManager(app)

SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Access API'
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

process3d = None
process2d = None
processCarla = None

number_of_vehicles = 0
blocked_roundabouts = []
blocked_roads = []
current_user = None
simulation_name = None
sim_running = False


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


@app.route('/user', methods=['GET'])
def get_user():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'message': 'Access Token is missing'}), 401

    token = auth_header.split(' ')[1]
    print(f"Token: {token}")
    try:
        decoded_token = decode_token(token)
        print(f"Decoded Token: {decoded_token}")
        email = decoded_token['sub']
        print(f"Email: {email}")
    except Exception as e:
        return jsonify({'message': 'Invalid token'}), 401

    user = mongo.db.users.find_one({'email': email})
    if not user:
        return jsonify({'message': 'User not found'}), 404

    response = json_util.dumps(user)
    return Response(response, mimetype="application/json")


@app.route('/api/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']

    user = mongo.db.users.find_one({'email': email})

    if not user:
        return jsonify({'message': 'User not found'}), 404

    if not check_password_hash(user['password'], password):
        return jsonify({'message': 'Incorrect password'}), 401

    access_token = create_access_token(identity=email)
    print(f"Access Token: {access_token}")

    global current_user
    current_user = user['email']

    response = make_response(
        jsonify({'message': 'Login successful', 'username': user['username'], 'token': access_token}), 200)
    response.headers['Authorization'] = f'Bearer {access_token}'
    return response


@app.route('/user', methods=['DELETE'])
def delete_user():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'message': 'Access Token is missing'}), 401

    token = auth_header.split(' ')[1]

    try:
        decoded_token = decode_token(token)
        email = decoded_token['sub']
    except Exception as e:
        return jsonify({'message': 'Invalid token'}), 401

    user = mongo.db.users.find_one({'email': email})
    if not user:
        return jsonify({'message': 'User not found'}), 404

    mongo.db.users.delete_one({'_id': ObjectId(user['_id'])})
    response = jsonify({'message': 'User ' + email + ' Deleted Successfully'})
    response.status_code = 200
    return response


@app.route('/user', methods=['PUT'])
def update_user():
    username = request.json['username']
    email = request.json['email']

    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'message': 'Access Token is missing'}), 401

    token = auth_header.split(' ')[1]
    print(f"Token: {token}")

    try:
        decoded_token = decode_token(token)
        print(f"Decoded Token: {decoded_token}")

        email = decoded_token['sub']
        print(f"Email: {email}")
    except Exception as e:
        return jsonify({'message': 'Invalid token'}), 401

    user = mongo.db.users.find_one({'email': email})
    print(f"User: {user}")
    if not user:
        return jsonify({'message': 'User not found'}), 404

    update_data = {}
    if username:
        update_data['username'] = username
    if email:
        update_data['email'] = email

    mongo.db.users.update_one(
        {'email': email},
        {'$set': update_data}
    )

    return jsonify({'message': 'User updated successfully'}), 200


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
    print("chegou no 3d 1")
    try:

        live = request.args.get('live', default=False)
        real_data = request.args.get('realdata', default=False)
        global processCarla
        global process3d
        print("chegou no 3d 2")

        if live == "True":
            print("chegou no 3d")
            processCarla = subprocess.Popen(["Adapters/co_simulation/runCarlaLive.sh"])
            sleep(10)
            process3d = subprocess.Popen(["python3", "Adapters/co_simulation/live_simulation3D.py", current_user])
            return jsonify({'message': 'Comando executado com sucesso'}), 200

        if real_data == "True":
            data = request.json
            entities = data.get('entities', [])
            day = data.get('day')
            start_time = data.get('startTime')
            end_time = data.get('endTime')

            # Aqui você pode usar os dados recebidos como desejar
            print(
                f"Recebido os seguintes dados: entities={entities}, day={day}, startTime={start_time}, endTime={end_time}")

            results = []

            for entity in entities:
                response = fetch_sth_comet_data(entity, start_time, end_time)
                if response.status_code == 200:
                    results.append(response.json())
                else:
                    print(f"Falha ao obter dados para {entity}: {response.text}")
            # print(results)
            realdata = RealData(start_time, results)
            realdata.iterate_data()
            for x in realdata.known_vehicle.keys():
                print("v:", x)
                realdata.create_vehicle(x)
                realdata.create_vehicle_route(x)

            realdata.tree.write(realdata.output_file)

            processCarla = subprocess.Popen(["Adapters/co_simulation/runCarla.sh"])
            sleep(10)

            process3d = subprocess.Popen(["python3", "Adapters/co_simulation/RealSimulation_3D.py", current_user])
            return jsonify({'message': 'Comando executado com sucesso'}), 200

        processCarla = subprocess.Popen(["Adapters/co_simulation/runCarla.sh"])
        sleep(10)

        process3d = subprocess.Popen(["python3", "Adapters/co_simulation/simulation_3D.py", current_user])
        return jsonify({'message': 'Comando executado com sucesso'}), 200



    except subprocess.CalledProcessError as e:
        return jsonify({'error': e}), 500


@app.route('/api/run2D', methods=['POST'])
def run_2D():
    try:
        print("entrou 2d")
        live = request.args.get('live', default=False)
        real_data = request.args.get('realdata', default=False)
        global process2d
        global blocked_roundabouts

        if live == "True":
            process2d = subprocess.Popen(["python3", "Adapters/co_simulation/live_simulation2D.py", current_user])
            blocked_roundabouts = []
            return jsonify({'message': 'Comando iniciado com sucesso'}), 200


        elif real_data == "True":
            data = request.json
            entities = data.get('entities', [])
            start_time = data.get('startTime')
            end_time = data.get('endTime')
            print(
                f" DENTRO DO RUN2D: Recebido os seguintes dados: entities={entities}, startTime={start_time}, endTime={end_time}")

            results = []

            for entity in entities:
                response = fetch_sth_comet_data(entity, start_time, end_time)
                if response.status_code == 200:
                    results.append(response.json())
                else:
                    print(f"Falha ao obter dados para {entity}: {response.text}")
            #print(results)
            realdata = RealData(start_time, results)
            realdata.iterate_data()
            for x in realdata.known_vehicle.keys():
                print("v:", x)
                realdata.create_vehicle(x)
                realdata.create_vehicle_route(x)

            realdata.tree.write(realdata.output_file)
            process2d = subprocess.Popen(["python3", "Adapters/co_simulation/RealSimulation_2D.py", current_user])

            return jsonify({'message': 'Dados históricos obtidos com sucesso'}), 200

        print("chamou 2d limpo")

        process2d = subprocess.Popen(["python3", "Adapters/co_simulation/simulation_2D.py", current_user])
        blocked_roundabouts = []

        return jsonify({'message': 'Comando iniciado com sucesso'}), 200

    except subprocess.CalledProcessError as e:
        return jsonify({'error': str(e)}), 500


def fetch_sth_comet_data(entity, start_time, end_time, lastN=1000):
    base_url = 'http://10.0.23.112:30866/STH/v2/entities/all/attrs/all'
    headers = {
        'fiware-service': 'default',
        'fiware-servicepath': '/atcll'
    }
    params = {
        'type': entity,
        'lastN': lastN,
        'dateFrom': f"{start_time}",
        'dateTo': f"{end_time}"
    }
    response = requests.get(base_url, headers=headers, params=params)
    #print(params)
    if response.status_code == 200:
        print(f"DENTRO DO FETCH: Requisição para {entity} retornou com sucesso")
    else:
        print(f"Falha ao obter dados para {entity}:")

    return response




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


@app.route('/api/addRandomPedestrian', methods=['POST'])
def add_random_pedestrian():
    qtd = request.args.get('qtd')
    if qtd is None:
        return jsonify({'error': 'Parâmetro "qtd" é obrigatório na URL'}), 400

    try:
        publish.single("/addRandomPedestrian", payload=f'{qtd}', hostname="localhost", port=1883)
        return jsonify({'message': f'Pedestres aleatórios adicionados para {qtd} pedestres'}), 200
    except Exception as e:
        return jsonify({'error': e}), 500

    # curl -X POST -d "" "http://localhost:5000/api/addRandomTraffic?qtd=500"


@app.route('/api/addRandomMotorcycle', methods=['POST'])
def add_random_motorcycle():
    qtd = request.args.get('qtd')
    if qtd is None:
        return jsonify({'error': 'Parâmetro "qtd" é obrigatório na URL'}), 400

    try:
        publish.single("/addRandomMotorcycle", payload=f'{qtd}', hostname="localhost", port=1883)
        return jsonify({'message': f'Motocicletas aleatórias adicionadas para {qtd} motocicletas'}), 200
    except Exception as e:
        return jsonify({'error': e}), 500


@app.route('/api/addRandomBike', methods=['POST'])
def add_random_bike():
    qtd = request.args.get('qtd')
    if qtd is None:
        return jsonify({'error': 'Parâmetro "qtd" é obrigatório na URL'}), 400

    try:
        publish.single("/addRandomBike", payload=f'{qtd}', hostname="localhost", port=1883)
        return jsonify({'message': f'Motocicletas aleatórias adicionadas para {qtd} motocicletas'}), 200
    except Exception as e:
        return jsonify({'error': e}), 500


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

    #curl -X POST -H "Content-Type: application/json" -d '{
    #"end": {"lng": "-8.655386132941464", "lat": "40.63525392116133"},
    #"start": {"lng": "-8.660106693274248", "lat": "40.635327506990194"}
    #}' http://localhost:5000/api/addSimulatedCar


@app.route('/api/endSimulation', methods=['POST'])
def end_simulation():
    publish.single("/endSimulation", payload="", hostname="localhost", port=1883)
    # try:
    #     if process2d is not None:
    #         process2d.send_signal(signal.SIGKILL)

    #     if process3d is not None:
    #         process3d.kill()

    #     if processCarla is not None:
    #         processCarla.send_signal(signal.SIGINT)

    global sim_running
    sim_running = False

    return jsonify({'message': 'Simulação finalizada com sucesso'}), 200
    # except Exception as e:
    #     return jsonify({'error': str(e)}), 500

    # curl -X POST -d "" "http://localhost:5000/api/endSimulation"


@app.route('/api/endSimulationAndSave', methods=['POST'])
def end_simulation_and_save():
    global simulation_name
    simulation_name = request.args.get('name')

    publish.single("/endSimulationAndSave", payload="", hostname="localhost", port=1883)

    global sim_running
    sim_running = False

    return jsonify({'message': 'Simulação finalizada e salva com sucesso'}), 200

    # curl -X POST -d "" "http://localhost:5000/api/endSimulationAndSave"


@app.route('/api/cars', methods=['POST'])
def cars():
    try:
        data = request.json
        print("Dados recebidos:", data)
        return jsonify({'message': 'Veículo adicionado com sucesso'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/clearSimulation', methods=['GET'])
def clear_simulation():
    try:
        publish.single("/clearSimulation", payload="", hostname="localhost", port=1883)
        return jsonify({'message': 'Simulação finalizada com sucesso'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # curl -X GET "http://localhost:5000/api/clearSimulation"


@app.route('/api/blockRoundabout', methods=['POST'])
def block_roundabout():
    roundabout_id = request.args.get('id')
    if roundabout_id is None:
        return jsonify({'error': 'Parâmetro "id" é obrigatório na URL'}), 400

    try:
        publish.single("/blockRoundabout", payload=roundabout_id, hostname="localhost", port=1883)
        return jsonify({'message': f'Rotunda {roundabout_id} bloqueada'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # curl -X POST -d "" "http://localhost:5000/api/blockRoundabout?id=1"


@app.route('/api/blockRoad', methods=['POST'])
def block_road():
    road_id = request.args.get('id')
    if road_id is None:
        return jsonify({'error': 'Parâmetro "id" é obrigatório na URL'}), 400

    try:
        publish.single("/blockRoad", payload=road_id, hostname="localhost", port=1883)
        return jsonify({'message': f'Estrada {road_id} bloqueada'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # curl -X POST -d "" "http://localhost:5000/api/blockRoad?id=1"


@app.route('/api/unblockRoundabout', methods=['POST'])
def unblock_roundabout():
    roundabout_id = request.args.get('id')
    if roundabout_id is None:
        return jsonify({'error': 'Parâmetro "id" é obrigatório na URL'}), 400

    try:
        publish.single("/unblockRoundabout", payload=roundabout_id, hostname="localhost", port=1883)
        return jsonify({'message': f'Rotunda {roundabout_id} desbloqueada'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # curl -X POST -d "" "http://localhost:5000/api/unblockRoundabout?id=1"


@app.route('/api/unblockRoad', methods=['POST'])
def unblock_road():
    road_id = request.args.get('id')
    if road_id is None:
        return jsonify({'error': 'Parâmetro "id" é obrigatório na URL'}), 400

    try:
        publish.single("/unblockRoad", payload=road_id, hostname="localhost", port=1883)
        return jsonify({'message': f'Estrada {road_id} desbloqueada'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # curl -X POST -d "" "http://localhost:5000/api/unblockRoad?id=1"


@app.route('/api/vehicles', methods=['GET'])
def get_vehicles():
    return jsonify({'quantity': number_of_vehicles})

    # curl -X GET "http://localhost:5000/api/vehicles"


@app.route('/api/blockedRoundabouts', methods=['GET'])
def get_blocked_roundabouts():
    return jsonify({'blocked_roundabouts': blocked_roundabouts})

    # curl -X GET "http://localhost:5000/api/blockedRoundabouts"


@app.route('/api/blockedRoads', methods=['GET'])
def get_blocked_roads():
    return jsonify({'blocked_roads': blocked_roads})

    # curl -X GET "http://localhost:5000/api/blockedRoads"


@app.route('/api/history', methods=['GET'])
def get_history_for_user():
    history = mongo.db.history.find({'user_email': current_user}, {'history': 0})
    response = json_util.dumps(history)

    return Response(response, mimetype="application/json")

    # curl -X GET "http://localhost:5000/api/history"


@app.route('/api/history', methods=['DELETE'])
def delete_history_for_user():
    _id = request.args.get('id')
    if _id is None:
        return jsonify({'error': 'Parâmetro "id" é obrigatório na URL'}), 400

    try:
        mongo.db.history.delete_one({'_id': ObjectId(_id)})
        return jsonify({'message': 'Histórico deletado com sucesso'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # curl -X DELETE "http://localhost:5000/api/history?id=1"


@app.route('/api/sim_running', methods=['GET'])
def is_simulation_running():
    return jsonify({'sim_running': sim_running})

    # curl -X GET "http://localhost:5000/api/sim_running"


@app.route('/api/resimulation', methods=['POST'])
def resimulation():
    # get the simulation id
    simulation_id = request.args.get('id')

    try:
        global process2d
        process2d = subprocess.Popen(["python3", "Adapters/co_simulation/simulation_2D.py", current_user,
                                      "--resimulation", simulation_id])
        global blocked_roundabouts
        blocked_roundabouts = []
        global sim_running
        sim_running = True

        return jsonify({'message': 'Comando iniciado com sucesso'}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({'error': e}), 500

    # curl -X POST -d "" "http://localhost:5000/api/resimulation?id=1"


def on_connect(client, userdata, flags, rc):
    print(f"Conectado ao broker com código de resultado {rc}")


def on_publish(client, userdata, mid):
    print("Mensagem publicada com sucesso (api)")


def on_message(client, userdata, msg):
    topic = msg.topic

    if topic == '/cars':
        ## usar socketio para enviar a mensagem para o front
        socketio.emit('cars', msg.payload)
        vehicle_data = json.loads(msg.payload)
        global number_of_vehicles
        number_of_vehicles = int(vehicle_data['vehicle']['quantity'])

    if topic == '/blocked_rounds':
        socketio.emit('blocked_roundabouts', msg.payload)
        blocked_roundabouts_data = json.loads(msg.payload)
        global blocked_roundabouts
        for roundabout in blocked_roundabouts_data['blocked_roundabouts'].keys():
            if roundabout not in blocked_roundabouts:
                blocked_roundabouts.append(roundabout)

    if topic == '/blocked_roads':
        socketio.emit('blocked_roads', msg.payload)
        blocked_roads_data = json.loads(msg.payload)
        global blocked_roads
        for road in blocked_roads_data['blocked_roads'].keys():
            if road not in blocked_roads:
                blocked_roads.append(road)

    if topic == '/history':
        data = {
            "user_email": json.loads(msg.payload)['user_email'],
            "history": json.loads(msg.payload)['history'],
            "date": datetime.now(),
            "simulation_name": simulation_name
        }
        mongo.db.history.insert_one(data)


def start_mqtt_connection():
    # Inicia a conexão MQTT
    mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_publish = on_publish
    mqtt_client.on_message = on_message
    mqtt_client.connect("localhost", 1883, 60)
    mqtt_client.subscribe("/cars")
    mqtt_client.subscribe("/blocked_rounds")
    mqtt_client.subscribe("/blocked_roads")
    mqtt_client.subscribe("/history")

    mqtt_client.loop_forever()  # Use loop_forever() para manter a conexão MQTT em execução indefinidamente


def start_flask():
    app.run(host='0.0.0.0')


if __name__ == '__main__':
    # Inicie a conexão MQTT em uma nova thread
    mqtt_thread = threading.Thread(target=start_mqtt_connection)
    mqtt_thread.start()

    # Inicie o Flask em uma nova thread
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.start()
