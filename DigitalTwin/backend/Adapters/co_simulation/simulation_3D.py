# ==================================================================================================
# -- imports ---------------------------------------------------------------------------------------
# ==================================================================================================

import argparse
import logging
import random
import time
import json
import os
import sys
import optparse
import threading
import sumolib
import traci    
import paho.mqtt.client as mqtt

file_path = os.path.join(os.path.dirname(__file__), "radar.json")
radar_file_path = os.path.join(os.path.dirname(__file__), "radar.json")
from coord_distance import calculate_bearing
roundabout_file_path = os.path.join(os.path.dirname(__file__), "roundabout.json")


# ==================================================================================================
# -- find carla module -----------------------------------------------------------------------------
# ==================================================================================================

import glob
import os
import sys

try:
    sys.path.append(
        glob.glob('/home/pi-digitaltwin/Desktop/CARLA/PythonAPI/carla/dist/carla-*%d.%d-%s.egg' %
                  (sys.version_info.major, sys.version_info.minor,
                   'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass


# ==================================================================================================
# -- sumo integration imports ----------------------------------------------------------------------
# ==================================================================================================

from sumo_integration.sumo_simulation import SumoSimulation  # pylint: disable=wrong-import-position
from sumo_integration.carla_simulation import CarlaSimulation  # pylint: disable=wrong-import-position
from modules.simulation_synchronization import SimulationSynchronization


net = sumolib.net.readNet(
    "Adapters/co_simulation/sumo_configuration/simple-map/UA.net.xml",
    withInternal=True)  # Carrega a rede do SUMO atraves do sumolib para acesso estatico




def synchronization_loop(args):
    """
    Entry point for sumo-carla co-simulation.
    """
    sumo_simulation = SumoSimulation(args.sumo_cfg_file, args.step_length, args.sumo_host,
                                     args.sumo_port, args.sumo_gui, args.client_order)
    carla_simulation = CarlaSimulation(args.carla_host, args.carla_port, args.step_length)

    synchronization = SimulationSynchronization(sumo_simulation, carla_simulation, args.tls_manager,
                                                args.sync_vehicle_color, args.sync_vehicle_lights)
    try:
        while True:

            start = time.time()

            synchronization.tick()


            end = time.time()
            elapsed = end - start
            if elapsed < args.step_length:
                time.sleep(args.step_length - elapsed)


            # if len(simulated_vehicles) > 0:
            #     for vehicle_id in list(simulated_vehicles.keys()):
            #         if vehicle_id in traci.vehicle.getIDList():
            #             checkDestination(vehicle_id, simulated_vehicles[vehicle_id])

    except KeyboardInterrupt:
        logging.info('Cancelled by user.')

    finally:
        logging.info('Cleaning synchronization')

        synchronization.close()




########### SUMOSUBSCRIBE


global step
allVehicle = set()
simulated_vehicles = {}
blocked_roundabouts = {}

randomVehiclesThread = None
end_addRandomTraffic = False

def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                          default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options


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

def unblockRoundabout(roundabout_id):
    global blocked_roundabouts
    for edge, speed in blocked_roundabouts[roundabout_id].items():
        traci.edge.setMaxSpeed(edge, speed)
    
    del blocked_roundabouts[roundabout_id]

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
            radar = data[1]
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
        # allVehicle.add(vehID)
        print(traci.vehicle.getRoute(vehID))
        print("adicionado")


def addSimulated(received):
    print(type(received))
    data = json.loads(received.decode('utf-8'))
    print("data", data.keys())

    if "start" in data.keys() and "end" in data.keys():
        logI, latI = data["start"]["lng"], data["start"]["lat"]
        logE, latE = data["end"]["lng"], data["end"]["lat"]

        Start = traci.simulation.convertRoad(float(logI), float(latI), isGeo=True, vClass="passenger")
        End = traci.simulation.convertRoad(float(logE), float(latE), isGeo=True, vClass="passenger")
        print("Start", Start)
        print("End", End)
        route = traci.simulation.findRoute(Start[0], End[0], getVtype(data["type"]))

        if route.edges:
            ts = str(time.time_ns())
            traci.route.add("route_simulated{}".format(ts), route.edges)
            traci.vehicle.add(vehID="simulated{}".format(ts), routeID="route_simulated{}".format(ts),
                              typeID=getVtype(data["type"]), depart=traci.simulation.getTime() + 2, departSpeed=0,
                              departLane="best")

            x, y = net.convertLonLat2XY(logI, latI)

            # Store destination
            x1, y1 = net.convertLonLat2XY(logE, latE)
            simulated_vehicles["simulated{}".format(ts)] = (x1, y1)

            traci.vehicle.moveToXY("simulated{}".format(ts), Start[0], 0, x, y, keepRoute=1)
        else:
            return "Não foi possível encontrar uma rota válida"



    elif "start" in data.keys():
        allowedEdges = [i.getID() for i in net.getEdges() if "driving" in i.getType()]
        randomEdge = random.choice(allowedEdges)
        print("random", randomEdge)
        logI, latI = data["start"]["lng"], data["start"]["lat"]

        print("logI: {}, latI: {}".format(logI, latI))

        Start = traci.simulation.convertRoad(float(logI), float(latI), isGeo=True, vClass="passenger")

        route = traci.simulation.findRoute(Start[0], randomEdge, getVtype(data["type"]))

        if route.edges:
            ts = str(time.time_ns())
            traci.route.add("route_simulated{}".format(ts), route.edges)
            traci.vehicle.add(vehID="simulated{}".format(ts), routeID="route_simulated{}".format(ts),
                              typeID=getVtype(data["type"]), depart=traci.simulation.getTime() + 2, departSpeed=0,
                              departLane="best")

            x, y = net.convertLonLat2XY(logI, latI)
            traci.vehicle.moveToXY("simulated{}".format(ts), Start[0], 0, x, y, keepRoute=1)

            # Store destination
            edge = net.getEdge(randomEdge)
            x1, y1 = edge.getShape()[0]
            simulated_vehicles["simulated{}".format(ts)] = (x1, y1)

        else:
            return "Não foi possível encontrar uma rota válida"


    elif "end" in data.keys():
        allowedEdges = [i.getID() for i in net.getEdges() if "driving" in i.getType()]
        randomEdge = random.choice(allowedEdges)
        logE, latE = data["end"]["lng"], data["end"]["lat"]

        print("logE: {}, latE: {}".format(logE, latE))

        End = traci.simulation.convertRoad(float(logE), float(latE), isGeo=True, vClass="passenger")

        route = traci.simulation.findRoute(randomEdge, End[0], getVtype(data["type"]))

        if route.edges:
            ts = str(time.time_ns())
            traci.route.add("route_simulated{}".format(ts), route.edges)
            traci.vehicle.add(vehID="simulated{}".format(ts), routeID="route_simulated{}".format(ts),
                              typeID=getVtype(data["type"]), depart=traci.simulation.getTime() + 2, departSpeed=0,
                              departLane="best")

            edge = net.getEdge(randomEdge)
            x, y = edge.getShape()[0]
            traci.vehicle.moveToXY("simulated{}".format(ts), randomEdge, 0, x, y, keepRoute=1)

            # Store destination
            x1, y1 = net.convertLonLat2XY(logE, latE)
            simulated_vehicles["simulated{}".format(ts)] = (x1, y1)

        else:
            return "Não foi possível encontrar uma rota válida"

def getVtype(vClass):
    if vClass == "car":
        return "vehicle.audi.a2"
    elif vClass == "motorcycle":
        return "vehicle.kawasaki.ninja"
    elif vClass == "bike":
        return "vehicle.bh.crossbike"

def addSimulatedPedestrian(received):
    print(type(received))
    data = json.loads(received.decode('utf-8'))
    print("data", data.keys())

    allowedEdges = [net.getLane(lane).getEdge() for lane in traci.lane.getIDList() if
                    net.getLane(lane).allows("pedestrian") and ":" not in lane and net.getLane(
                        lane).getEdge().getLaneNumber() > 1]



    if "start" in data.keys() and "end" in data.keys():
        logI, latI = data["start"]["lng"], data["start"]["lat"]
        logE, latE = data["end"]["lng"], data["end"]["lat"]

        person_id = "randomPedestrian_{}".format(time.time_ns())
        Start = traci.simulation.convertRoad(float(logI), float(latI), isGeo=True, vClass="pedestrian")
        End = traci.simulation.convertRoad(float(logE), float(latE), isGeo=True, vClass="pedestrian")
        print("Start", Start)
        print("End", End)
        route = traci.simulation.findIntermodalRoute(Start[0], End[0], pType="DEFAULT_PEDTYPE")

        if route[0].edges:
            traci.person.add(person_id, Start[0], pos=0)
            traci.person.appendWalkingStage(person_id, route[0].edges, arrivalPos=0)
        else:
            return "Não foi possível encontrar uma rota válida"

    elif "start" in data.keys():
        logI, latI = data["start"]["lng"], data["start"]["lat"]
        print("logI: {}, latI: {}".format(logI, latI))

        person_id = "randomPedestrian_{}".format(time.time_ns())
        Start = traci.simulation.convertRoad(float(logI), float(latI), isGeo=True, vClass="pedestrian")
        route = traci.simulation.findIntermodalRoute(Start[0], random.choice(allowedEdges), pType="DEFAULT_PEDTYPE")

        if route[0].edges:
            traci.person.add(person_id, Start[0], pos=0)
            traci.person.appendWalkingStage(person_id, route[0].edges, arrivalPos=0)
        else:
            return "Não foi possível encontrar uma rota válida"

    elif "end" in data.keys():
        logE, latE = data["end"]["lng"], data["end"]["lat"]

        person_id = "randomPedestrian_{}".format(time.time_ns())
        End = traci.simulation.convertRoad(float(logE), float(latE), isGeo=True, vClass="pedestrian")
        route = traci.simulation.findIntermodalRoute(random.choice(allowedEdges), End[0], pType="DEFAULT_PEDTYPE")

        if route[0].edges:
            traci.person.add(person_id, random.choice(allowedEdges), pos=0)
            traci.person.appendWalkingStage(person_id, route[0].edges, arrivalPos=0)
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
            route = traci.simulation.findIntermodalRoute(start, end, pType="walker.pedestrian.0001")
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

def endSimulation():
    traci.close()
    sys.stdout.flush()


def on_connect(client, userdata, flags, rc):
    print(f"Conectado ao broker com código de resultado {rc}")



def on_publish(client, userdata, mid):
    print("Mensagem publicada com sucesso")

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


    if topic == "/addSimulated":
        print("entrou", topic)
        print(msg.payload)
        payload = msg.payload
        addSimulated(payload)

    if topic == "/addSimulatedPedestrian":
        print("entrou", topic)
        print(msg.payload)
        payload = msg.payload
        addSimulatedPedestrian(payload)

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
        clearSimulation()

    if topic == "/endSimulation":
        print("Ending simulation...")
        endSimulation()
        print("Simulation ended")

    if topic == "/blockRoundabout":
        payload = json.loads(msg.payload)
        blockRoundabout(int(payload))

    if topic == "/unblockRoundabout":
        payload = json.loads(msg.payload)
        unblockRoundabout(int(payload))


def synchronization_loop_wrapper(arguments):
    synchronization_loop(arguments)

if __name__ == "__main__":
    class StaticArguments:
        def __init__(self):
            self.sumo_cfg_file = "Adapters/co_simulation/sumo_configuration/simple-map/simple-map.sumocfg"
            self.carla_host = '127.0.0.1'
            self.carla_port = 2000
            self.sumo_host = None
            self.sumo_port = None
            self.sumo_gui = True
            self.step_length = 0.05
            self.client_order = 1
            self.sync_vehicle_lights = False
            self.sync_vehicle_color = False
            self.sync_vehicle_all = False
            self.tls_manager = 'carla'
            self.debug = False


    # Cria uma instância dos argumentos estáticos
    arguments = StaticArguments()

    if arguments.sync_vehicle_all is True:
        arguments.sync_vehicle_lights = True
        arguments.sync_vehicle_color = True

    if arguments.debug:
        logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    else:
        logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

    print("teste")
    synchronization_thread = threading.Thread(target=synchronization_loop_wrapper, args=[arguments])
    synchronization_thread.start()

    
    print("teste2")
    # Inicia a conexão MQTT
    mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_publish = on_publish
    mqtt_client.on_message = on_message
    mqtt_client.connect("localhost", 1883, 60)
    mqtt_client.subscribe("/realDatateste")
    mqtt_client.subscribe("/addRandomTraffic")
    mqtt_client.subscribe("/addRandomPedestrian")
    mqtt_client.subscribe("/addSimulated")
    mqtt_client.subscribe("/addSimulatedPedestrian")
    mqtt_client.subscribe("/endSimulation")
    mqtt_client.subscribe("/addRandomMotorcycle")
    mqtt_client.subscribe("/addRandomBike")
    mqtt_client.subscribe("/clearSimulation")
    mqtt_client.subscribe("/blockRoundabout")
    mqtt_client.subscribe("/unblockRoundabout")

    
    mqtt_thread = threading.Thread(target=mqtt_client.loop_start)
    mqtt_thread.start()

