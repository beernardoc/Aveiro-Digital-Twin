import json
import random
import optparse
import threading
import time

import sumolib
import traci
import sys
import getopt
import os

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

from pymongo import MongoClient
from bson import ObjectId
from traci.exceptions import TraCIException

# Determine the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if project_root not in sys.path:
    sys.path.append(project_root)
from Adapters.history.file_composer import FileComposer

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
radar_file_path = os.path.join(os.path.dirname(__file__), "radar.json")
roundabout_file_path = os.path.join(os.path.dirname(__file__), "roundabout.json")
road_file_path = os.path.join(os.path.dirname(__file__), "road.json")
from coord_distance import calculate_bearing

mongo_client = MongoClient(host='localhost', port=27017, username='admin', password='password')
mongo = mongo_client['digitaltwin']

def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                          default=False, help="run the commandline version of sumo")
    opt_parser.add_option("--resimulation", action="store", type="string",
                          help="run a resimulation with the given history id")
    options, args = opt_parser.parse_args()
    return options


global step
simulated_vehicles = {}
blocked_roundabouts = {}
blocked_roads = {}
all_vehicles = {}

current_user = None
if len(sys.argv) > 1:
    current_user = sys.argv[1]

randomVehiclesThread = None
end_addRandomTraffic = False

net = sumolib.net.readNet(
    "Adapters/co_simulation/sumo_configuration/simple-map/UA.net.xml",
    withInternal=True)  # Carrega a rede do SUMO atraves do sumolib para acesso estatico

history_file = FileComposer("Adapters/history/base_file.xml")

def run():
    step = 0
    while True:
        try:
            traci.simulationStep()

            for vehicle_id in traci.vehicle.getIDList():
                vehicle_type = traci.vehicle.getTypeID(vehicle_id)
                depart = str(round(step, 1))
                route = traci.vehicle.getRoute(vehicle_id)
                if vehicle_id not in all_vehicles:
                    all_vehicles[vehicle_id] = {"type": vehicle_type, "depart": depart, "route": route}
                    # print(f'Vehicle {vehicle_id} added to the list of all vehicles. Type: {vehicle_type}, Depart: {depart}, Route: {route}')
                else:
                    if all_vehicles[vehicle_id]["route"] != route:
                        all_vehicles[vehicle_id]["route"] = route
                        # print(f'Vehicle {vehicle_id} changed route to {route}')

            step += 1

            simulation_time = traci.simulation.getTime()
            vehicles = traci.vehicle.getIDList()
            vehicle_type = traci.vehicletype.getIDList()
            person = traci.person.getIDList()

            data = {"vehicle": {"quantity": len(vehicles), "ids": vehicles},
                    "person": {"quantity": len(person), "ids": person},
                    "simulation": {"time": simulation_time, "vehicles_types": vehicle_type}}
            
            publish.single("/cars", payload=json.dumps(data), hostname="localhost", port=1883)

            global blocked_roundabouts
            global blocked_roads

            data = {"blocked_roundabouts": blocked_roundabouts}
            publish.single("/blocked_rounds", payload=json.dumps(data), hostname="localhost", port=1883)

            data = {"blocked_roads": blocked_roads}
            publish.single("/blocked_roads", payload=json.dumps(data), hostname="localhost", port=1883)

            # if len(simulated_vehicles) > 0:
            #     for vehicle_id in list(simulated_vehicles.keys()):
            #         if vehicle_id in traci.vehicle.getIDList():
            #             checkDestination(vehicle_id, simulated_vehicles[vehicle_id])

        except Exception as e:
            print(e)
            break


def checkDestination(vehicle_id, destination_coordinates):
    global simulated_vehicles
    # Check if vehicle is in the list of simulated vehicles and is still in the simulation
    if vehicle_id in simulated_vehicles and vehicle_id in traci.vehicle.getIDList():
        vehicle_position = traci.vehicle.getPosition(vehicle_id)

        if vehicle_position is not None:
            distance_to_destination = traci.simulation.getDistance2D(float(vehicle_position[0]),
                                                                     float(vehicle_position[1]),
                                                                     float(destination_coordinates[0]),
                                                                     float(destination_coordinates[1]))

            #print("{} - Distance to destination: {}".format(vehicle_id, distance_to_destination))
            if distance_to_destination < 6:  # 6 meters from destination (MUDAR COMO ACHARMOS MELHOR)
                traci.vehicle.remove(vehicle_id)
                simulated_vehicles.pop(vehicle_id, None)
                print("Vehicle {} has reached its destination.".format(vehicle_id))
    else:
        print("Vehicle {} not found in the list of simulated vehicles.".format(vehicle_id))

def blockRoundabout(roundabout_id):
    with open(roundabout_file_path, "r") as f:
        data = json.load(f)
        roundabout = data[roundabout_id - 1]
        f.close()

    global blocked_roundabouts
    blocked_roundabouts[roundabout_id] = {}

    for edge in roundabout["edges"]:
        all_lane_ids = traci.lane.getIDList()
        lanes = [lane for lane in all_lane_ids if lane.startswith(str(edge) + "_")]
        max_speed = 0
        for lane in lanes:
            if max_speed < traci.lane.getMaxSpeed(lane):
                max_speed = traci.lane.getMaxSpeed(lane)
        blocked_roundabouts[roundabout_id][edge] = max_speed
        traci.edge.setMaxSpeed(edge, 0)

def blockRoad(road_id):
    with open(road_file_path, "r") as f:
        data = json.load(f)
        road = data[str(road_id)]
        f.close()

    global blocked_roads
    blocked_roads[road_id] = {}
    
    for edge in road["edges"]:
        all_lane_ids = traci.lane.getIDList()
        lanes = [lane for lane in all_lane_ids if lane.startswith(str(edge) + "_")]
        max_speed = 0
        for lane in lanes:
            if max_speed < traci.lane.getMaxSpeed(lane):
                max_speed = traci.lane.getMaxSpeed(lane)
        blocked_roads[road_id][edge] = max_speed
        traci.edge.setMaxSpeed(edge, 0)

def unblockRoundabout(roundabout_id):
    global blocked_roundabouts
    for edge, speed in blocked_roundabouts[roundabout_id].items():
        traci.edge.setMaxSpeed(edge, speed)
    
    del blocked_roundabouts[roundabout_id]

def unblockRoad(road_id):
    global blocked_roads
    for edge, speed in blocked_roads[road_id].items():
        traci.edge.setMaxSpeed(edge, speed)
    
    del blocked_roads[road_id]

def clearSimulation():
    time.sleep(3)
    vehicles = traci.vehicle.getIDList()
    for vehicle in vehicles:
        traci.vehicle.remove(vehicle)


def addOrUpdateRealCar(received):
    print("received", received)
    log, lat, heading = received["longitude"], received["latitude"], received["heading"]
    print("log: {}, lat: {}, heading: {}".format(log, lat, heading))

    vehID = str(received["objectID"])
    x, y = net.convertLonLat2XY(log, lat)  # Converte as coordenadas para o sistema de coordenadas do SUMO
    allCars = traci.vehicle.getIDList()

    if vehID in allCars:
        new_speed = received["speed"]
        traci.vehicle.setSpeed(vehID, new_speed)


    else:  # Adiciona um novo veículo
        # if the heading is positive it is directed to the sensor, if it is negative it is directed away from the sensor
        # get the sensor information from radar.json
        with open(radar_file_path, "r") as f:
            data = json.load(f)
            radar = data[2]
            # get the angle from the sensor to the vehicle
            angle = calculate_bearing((radar['coord']['lat'], radar['coord']['lng']), (lat, log))
            if radar['angle_type'] == 0:
                if 0 <= angle <= 90 or 270 <= angle <= 360:
                    if heading < 0:
                        route = radar['lanes']['near']
                    else:
                        route = radar['lanes']['far']

                else:
                    if heading < 0:
                        route = radar['lanes']['far']
                    else:
                        route = radar['lanes']['near']

            elif radar['angle_type'] == 1:
                if 0 <= angle <= 90 or 270 <= angle <= 360:
                    if heading < 0:
                        route = radar['lanes']['far']
                    else:
                        route = radar['lanes']['near']

                else:
                    if heading < 0:
                        route = radar['lanes']['near']
                    else:
                        route = radar['lanes']['far']
            f.close()

        traci.route.add(routeID=("route_" + vehID), edges=route)  # adiciona uma rota para o veículo
        traci.vehicle.add(vehID, routeID=("route_" + vehID), typeID="vehicle.audi.a2",
                          depart=traci.simulation.getTime() + 1, departSpeed=0,
                          departLane="best")
        traci.vehicle.moveToXY(vehID, route[0], 0, x, y,
                               keepRoute=1)  # se a proxima for a mesma, cluster ou de junção, move com moveTOXY
        print(traci.vehicle.getRoute(vehID))
        print("adicionado")


def addSimulatedCar(received):
    print(type(received))
    data = json.loads(received.decode('utf-8'))
    print("data", data.keys())

    if data.keys() == {"start", "end"}:
        logI, latI = data["start"]["lng"], data["start"]["lat"]
        logE, latE = data["end"]["lng"], data["end"]["lat"]

        Start = traci.simulation.convertRoad(float(logI), float(latI), isGeo=True, vClass="passenger")
        End = traci.simulation.convertRoad(float(logE), float(latE), isGeo=True, vClass="passenger")
        print("Start", Start)
        print("End", End)
        route = traci.simulation.findRoute(Start[0], End[0], "vehicle.audi.a2")

        if route.edges:
            ts = str(time.time_ns())
            traci.route.add("route_simulated{}".format(ts), route.edges)
            traci.vehicle.add(vehID="simulated{}".format(ts), routeID="route_simulated{}".format(ts),
                              typeID="vehicle.audi.a2", depart=traci.simulation.getTime() + 2, departSpeed=0,
                              departLane="best")

            x, y = net.convertLonLat2XY(logI, latI)

            # Store destination
            x1, y1 = net.convertLonLat2XY(logE, latE)
            simulated_vehicles["simulated{}".format(ts)] = (x1, y1)

            traci.vehicle.moveToXY("simulated{}".format(ts), Start[0], 0, x, y, keepRoute=1)
        else:
            return "Não foi possível encontrar uma rota válida"





    elif data.keys() == {"start"}:
        allowedEdges = [i.getID() for i in net.getEdges() if "driving" in i.getType()]
        randomEdge = random.choice(allowedEdges)
        print("random", randomEdge)
        logI, latI = data["start"]["lng"], data["start"]["lat"]

        print("logI: {}, latI: {}".format(logI, latI))

        Start = traci.simulation.convertRoad(float(logI), float(latI), isGeo=True, vClass="passenger")

        route = traci.simulation.findRoute(Start[0], randomEdge, "vehicle.audi.a2")

        if route.edges:
            ts = str(time.time_ns())
            traci.route.add("route_simulated{}".format(ts), route.edges)
            traci.vehicle.add(vehID="simulated{}".format(ts), routeID="route_simulated{}".format(ts),
                              typeID="vehicle.audi.a2", depart=traci.simulation.getTime() + 2, departSpeed=0,
                              departLane="best")

            x, y = net.convertLonLat2XY(logI, latI)
            traci.vehicle.moveToXY("simulated{}".format(ts), Start[0], 0, x, y, keepRoute=1)

            # Store destination
            edge = net.getEdge(randomEdge)
            x1, y1 = edge.getShape()[0]
            simulated_vehicles["simulated{}".format(ts)] = (x1, y1)

        else:
            return "Não foi possível encontrar uma rota válida"


    elif data.keys() == {"end"}:
        allowedEdges = [i.getID() for i in net.getEdges() if "driving" in i.getType()]
        randomEdge = random.choice(allowedEdges)
        logE, latE = data["end"]["lng"], data["end"]["lat"]

        print("logE: {}, latE: {}".format(logE, latE))

        End = traci.simulation.convertRoad(float(logE), float(latE), isGeo=True, vClass="passenger")

        route = traci.simulation.findRoute(randomEdge, End[0], "vehicle.audi.a2")

        if route.edges:
            ts = str(time.time_ns())
            traci.route.add("route_simulated{}".format(ts), route.edges)
            traci.vehicle.add(vehID="simulated{}".format(ts), routeID="route_simulated{}".format(ts),
                              typeID="vehicle.audi.a2", depart=traci.simulation.getTime() + 2, departSpeed=0,
                              departLane="best")

            edge = net.getEdge(randomEdge)
            x, y = edge.getShape()[0]
            traci.vehicle.moveToXY("simulated{}".format(ts), randomEdge, 0, x, y, keepRoute=1)

            # Store destination
            x1, y1 = net.convertLonLat2XY(logE, latE)
            simulated_vehicles["simulated{}".format(ts)] = (x1, y1)

        else:
            return "Não foi possível encontrar uma rota válida"


def addRandomTraffic(QtdCars):
    allowedEdges = [i.getID() for i in net.getEdges() if "driving" in i.getType()]
    types = traci.vehicletype.getIDList()
    if len(allowedEdges) != 0:
        for count in range(QtdCars):
            global end_addRandomTraffic
            if end_addRandomTraffic:
                break
            routeID = "route_{}".format(time.time_ns())
            vehicle_id = "randomCar_{}".format(time.time_ns())
            #typeID = random.choice(types)
            #if typeID == "DEFAULT_PEDTYPE":
            #    typeID = "DEFAULT_VEHTYPE"
            route = traci.simulation.findRoute(random.choice(allowedEdges), random.choice(allowedEdges),
                                               "vehicle.dodge.charger_police_2020")
            if route.edges:
                traci.route.add(routeID, route.edges)
                traci.vehicle.add(vehicle_id, routeID, "vehicle.dodge.charger_police_2020", depart="now", departSpeed=0,
                                  departLane="best", )


def addRandomPedestrian(QtdPerson):  #TODO: melhorar o findroute
    allowedEdges = [net.getLane(lane).getEdge() for lane in traci.lane.getIDList() if
                    net.getLane(lane).allows("pedestrian") and ":" not in lane and net.getLane(
                        lane).getEdge().getLaneNumber() > 1]

    for count in range(QtdPerson):

        try:
            person_id = "randomPedestrian_{}".format(time.time_ns())
            start = random.choice(allowedEdges).getID()
            end = random.choice(allowedEdges).getID()
            #route = traci.simulation.findRoute(start, end)
            route = traci.simulation.findIntermodalRoute(start, end, pType="DEFAULT_PEDTYPE")
            print(route[0].edges)
            if route[0].edges:
                traci.person.add(person_id, start, pos=0)
                traci.person.appendWalkingStage(person_id, route[0].edges, arrivalPos=0)

        except Exception as e:
            print(e)
            continue


def addRandomMotorcycle(QtdMotorcycle):
    allowedEdges = [i.getID() for i in net.getEdges() if "driving" in i.getType()]
    for count in range(QtdMotorcycle):
        routeID = "route_{}".format(time.time_ns())
        vehicle_id = "randomMotorcycle_{}".format(time.time_ns())
        route = traci.simulation.findRoute(random.choice(allowedEdges), random.choice(allowedEdges),
                                           "vehicle.kawasaki.ninja")
        if route.edges:
            traci.route.add(routeID, route.edges)
            traci.vehicle.add(vehicle_id, routeID, "vehicle.kawasaki.ninja", depart="now", departSpeed=0,
                              departLane="best", )


def addRandomBike(QtdBike):
    allowedEdges = [i.getID() for i in net.getEdges() if "driving" in i.getType()]
    for count in range(QtdBike):
        routeID = "route_{}".format(time.time_ns())
        vehicle_id = "randomBike_{}".format(time.time_ns())
        route = traci.simulation.findRoute(random.choice(allowedEdges), random.choice(allowedEdges),
                                           "vehicle.gazelle.omafiets")
        if route.edges:
            traci.route.add(routeID, route.edges)
            traci.vehicle.add(vehicle_id, routeID, "vehicle.gazelle.omafiets", depart="now", departSpeed=0,
                              departLane="best", )

def endSimulation(save_history=False):
    
    if save_history:
        for vehicle_id, vehicle_info in all_vehicles.items():
            vehicle = { "id": vehicle_id, "type": vehicle_info["type"], "depart": vehicle_info["depart"] }
            route = list(vehicle_info["route"])
            history_file.add_vehicle(vehicle, route)

        data = {"user_email": current_user, "history": history_file.get_result_string()}
        publish.single("/history", payload=json.dumps(data), hostname="localhost", port=1883)

    traci.close()
    sys.stdout.flush()

def on_connect(client, userdata, flags, rc):
    print(f"Conectado ao broker com código de resultado {rc}")


def on_publish(client, userdata, mid):
    print("Mensagem publicada com sucesso (simulation)")


allCars = set()


def on_message(client, userdata, msg):
    topic = msg.topic
    print(topic)

    if topic == "/addRandomTraffic":
        payload = json.loads(msg.payload)
        try:
            # create a new thread to add random traffic
            global randomVehiclesThread
            randomVehiclesThread = threading.Thread(target=addRandomTraffic, args=[int(payload)])
            randomVehiclesThread.start()
        except Exception as e:
            print(e)
    if topic == "/addRandomPedestrian":
        print("entrou", topic)
        payload = json.loads(msg.payload)
        try:
            # create a new thread to add random traffic
            global randomPedestriansThread
            randomPedestriansThread = threading.Thread(target=addRandomPedestrian, args=[int(payload)])
            randomPedestriansThread.start()
        except Exception as e:
            print(e)

    if topic == "/addRandomMotorcycle":
        payload = json.loads(msg.payload)
        try:
            # create a new thread to add random traffic
            global randomMotorcycleThread
            randomMotorcycleThread = threading.Thread(target=addRandomMotorcycle, args=[int(payload)])
            randomMotorcycleThread.start()
        except Exception as e:
            print(e)



    if topic == "/addRandomBike":
        payload = json.loads(msg.payload)
        try:
            # create a new thread to add random traffic
            global randomBikeThread
            randomBikeThread = threading.Thread(target=addRandomBike, args=[int(payload)])
            randomBikeThread.start()
        except Exception as e:
            print(e)


    if topic == "/addSimulatedCar":
        print("entrou", topic)
        print(msg.payload)
        payload = msg.payload
        addSimulatedCar(payload)

    if topic == "/clearSimulation":
        print("Clearing simulation...")
        # stop the thread that adds random traffic
        global end_addRandomTraffic
        end_addRandomTraffic = True
        if randomVehiclesThread is not None:
            randomVehiclesThread.join()
        clearSimulation()
        print("Simulation cleared")
        end_addRandomTraffic = False

    if topic == "/endSimulation":
        print("Ending simulation...")
        endSimulation(False)
        print("Simulation ended")

    if topic == "/endSimulationAndSave":
        print("Ending simulation and saving history...")
        endSimulation(True)
        print("Simulation ended and history saved")

    if topic == "/blockRoundabout":
        payload = json.loads(msg.payload)
        blockRoundabout(int(payload))

    if topic == "/blockRoad":
        payload = json.loads(msg.payload)
        blockRoad(int(payload))

    if topic == "/unblockRoundabout":
        payload = json.loads(msg.payload)
        unblockRoundabout(int(payload))

    if topic == "/unblockRoad":
        payload = json.loads(msg.payload)
        unblockRoad(int(payload))

if __name__ == "__main__":
    options = get_options()
    if options.nogui:
        sumoBinary = sumolib.checkBinary('sumo')
    else:
        sumoBinary = sumolib.checkBinary('sumo-gui')

    if options.resimulation:
        _id = options.resimulation
        simulation = mongo.db.history.find_one({'_id': ObjectId(_id)})
        sim_xml = simulation["history"]
        # write to new rou file
        with open("Adapters/co_simulation/sumo_configuration/simple-map/resimulation.rou.xml", "w") as f:
            f.write(sim_xml)
            f.close()
        
        sumo_thread = threading.Thread(target=traci.start, args=[
            [sumoBinary, "-c", "Adapters/co_simulation/sumo_configuration/simple-map/resimulation.sumocfg",
            "--tripinfo-output",
            "tripinfo.xml",
            "--quit-on-end"
            ]])
        
    else:
        sumo_thread = threading.Thread(target=traci.start, args=[
            [sumoBinary, "-c", "Adapters/co_simulation/sumo_configuration/simple-map/simple-map.sumocfg",
            "--tripinfo-output",
            "tripinfo.xml",
            "--quit-on-end"
            ]])

    # Simple sumo network
    # sumo_thread = threading.Thread(target=traci.start, args=[
    #     [sumoBinary, "-c", "../simple_sumo_network/osm.sumocfg", "--tripinfo-output", "simple_tripinfo.xml"]])
    sumo_thread.start()
    # Executa a função run (controle do SUMO) após o início do SUMO
    sumo_thread.join()  # Aguarda até que o SUMO esteja pronto

    # Inicia a conexão MQTT
    mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_publish = on_publish
    mqtt_client.on_message = on_message
    mqtt_client.connect("localhost", 1883, 60)
    mqtt_client.subscribe("/realDatateste")
    mqtt_client.subscribe("/addRandomTraffic")
    mqtt_client.subscribe("/addRandomPedestrian")
    mqtt_client.subscribe("/addSimulatedCar")
    mqtt_client.subscribe("/endSimulation")
    mqtt_client.subscribe("/endSimulationAndSave")
    mqtt_client.subscribe("/addRandomMotorcycle")
    mqtt_client.subscribe("/addRandomBike")
    mqtt_client.subscribe("/clearSimulation")
    mqtt_client.subscribe("/blockRoundabout")
    mqtt_client.subscribe("/blockRoad")
    mqtt_client.subscribe("/unblockRoundabout")
    mqtt_client.subscribe("/unblockRoad")

    mqtt_thread = threading.Thread(target=mqtt_client.loop_start)
    mqtt_thread.start()



    run()
