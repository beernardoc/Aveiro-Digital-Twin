import json
import random
import optparse
import threading
import time

import sumolib
import traci
import sys
import os

import paho.mqtt.client as mqtt


sys.path.append(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(os.path.dirname(__file__), "radar.json")
from coord_distance import calculate_bearing


def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                          default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options


global step
lista = {}


def run():
    step = 0
    while True:

        traci.simulationStep()


        step += 1


    traci.close()
    sys.stdout.flush()


def addOrUpdateRealCar(received):
    print("received", received)
    log, lat, heading = received["longitude"], received["latitude"], received["heading"]
    print("log: {}, lat: {}, heading: {}".format(log, lat, heading))
    # if the heading is positive it is directed to the sensor, if it is negative it is directed away from the sensor
    # get the sensor information from radar.json
    with open(file_path, "r") as f:
        data = json.load(f)
        radar = data[0]
        # get the angle from the sensor to the vehicle
        angle = calculate_bearing((radar['coord']['lat'], radar['coord']['lng']), (lat, log))
        if radar['angle_type'] == 0:
            if 0 <= angle <= 90 or 270 <= angle <= 360:
                if heading < 0:
                    nextEdge = radar['lanes']['near']
                else:
                    nextEdge = radar['lanes']['far']
            else:
                if heading < 0:
                    nextEdge = radar['lanes']['far']
                else:
                    nextEdge = radar['lanes']['near']
        f.close()



    vehID = str(received["objectID"])
    x, y = net.convertLonLat2XY(log, lat) # Converte as coordenadas para o sistema de coordenadas do SUMO
    nextEdge = str(nextEdge)
    allCars = traci.vehicle.getIDList()
    print("next", nextEdge)

    if vehID in allCars:
        print(traci.vehicle.getRoadID(vehID))
        if traci.vehicle.getRoadID(vehID) == nextEdge or nextEdge.startswith(":cluster") or "_" in nextEdge:

            traci.vehicle.setSpeed(vehID, 10)
            global count
            if count >= 15 :
                traci.vehicle.setSpeed(vehID, 10)
            elif count > 10:
                traci.vehicle.setSpeed(vehID, 0)

            count += 1
            print(count)

        else:
            traci.vehicle.changeTarget(vehID, nextEdge) # se a proxima aresta for diferente, muda a rota
            print("mudou", traci.vehicle.getRoute(vehID))


    else: # Adiciona um novo veículo
        traci.route.add(routeID=("route_" + vehID), edges=[nextEdge]) # adiciona uma rota para o veículo
        traci.vehicle.add(vehID, routeID=("route_" + vehID), typeID="vehicle.audi.a2", depart="now", departSpeed=0, departLane="best")
        traci.vehicle.moveToXY(vehID, nextEdge, 0, x, y, keepRoute=1) # se a proxima for a mesma, cluster ou de junção, move com moveTOXY
        print(traci.vehicle.getRoute(vehID))
        print("adicionado")



def addSimulatedCar(received):
    print(type(received))
    data = json.loads(received.decode('utf-8'))
    print("data", data.keys())

    if data.keys() == {"start", "end"}:
        logI, latI = data["start"]["log"], data["start"]["lat"]
        logE, latE = data["end"]["log"], data["end"]["lat"]

        print("logI: {}, latI: {}".format(logI, latI))
        print("logE: {}, latE: {}".format(logE, latE))


        Start = traci.simulation.convertRoad(float(logI), float(latI), isGeo=True, vClass="passenger")
        End = traci.simulation.convertRoad(float(logE), float(latE), isGeo=True, vClass="passenger")

        print("Start", Start)
        print("End", End)
        ts = str(time.time_ns())
        traci.route.add("route_simulated{}".format(ts), [Start[0], End[0]])

        traci.vehicle.add(vehID="simulated{}".format(ts), routeID="route_simulated{}".format(ts),
                          typeID="vehicle.audi.a2", depart="now", departSpeed=0, departLane="best")
        return "Veículo adicionado com informações de início e fim"

    elif data.keys() == {"start"}:
        allowedEdges = [i.getID() for i in net.getEdges() if "driving" in i.getType()]
        randomEdge = random.choice(allowedEdges)
        logI, latI = data["start"]["log"], data["start"]["lat"]

        print("logI: {}, latI: {}".format(logI, latI))

        Start = traci.simulation.convertRoad(float(logI), float(latI), isGeo=True, vClass="passenger")

        print("Start", Start)
        ts = str(time.time_ns())
        traci.route.add("route_simulated{}".format(ts), [Start[0], randomEdge])

        traci.vehicle.add(vehID="simulated{}".format(ts), routeID="route_simulated{}".format(ts),
                          typeID="vehicle.audi.a2", depart="now", departSpeed=0, departLane="best")
        return "Veículo adicionado com informações de início"

    elif data.keys() == {"end"}:
        allowedEdges = [i.getID() for i in net.getEdges() if "driving" in i.getType()]
        randomEdge = random.choice(allowedEdges)
        logE, latE = data["end"]["log"], data["end"]["lat"]

        print("logE: {}, latE: {}".format(logE, latE))

        End = traci.simulation.convertRoad(float(logE), float(latE), isGeo=True, vClass="passenger")

        print("End", End)
        ts = str(time.time_ns())
        traci.route.add("route_simulated{}".format(ts), [randomEdge, End[0]])

        traci.vehicle.add(vehID="simulated{}".format(ts), routeID="route_simulated{}".format(ts),
                          typeID="vehicle.audi.a2", depart="now", departSpeed=0, departLane="best")
        return "Veículo adicionado com informações de fim"




def addRandomTraffic(QtdCars):
    allowedEdges = [i.getID() for i in net.getEdges() if "driving" in i.getType()]
    print(allowedEdges)
    if len(allowedEdges) != 0:

        for count in range(QtdCars):
            routeID = "route_{}".format(time.time_ns())
            vehicle_id = "random_{}".format(time.time_ns())
            route = traci.simulation.findRoute(random.choice(allowedEdges), random.choice(allowedEdges), vType="vehicle.audi.a2")
            if route.edges:
                traci.route.add(routeID, route.edges)
                traci.vehicle.add(vehicle_id, routeID, typeID="vehicle.audi.a2", depart="now", departSpeed=0,
                              departLane="best", )


def endSimulation():
    traci.close()
    sys.stdout.flush()





def on_connect(client, userdata, flags, rc):
    print(f"Conectado ao broker com código de resultado {rc}")


def on_publish(client, userdata, mid):
    print("Mensagem publicada com sucesso")


def on_message(client, userdata, msg):
    topic = msg.topic
    print(topic)
    if topic == "/realDatateste": # TODO: Mudar para topico real
        payload = json.loads(msg.payload)
        addOrUpdateRealCar(payload)
    if topic == "/addRandomTraffic":
        payload = json.loads(msg.payload)
        try:
            addRandomTraffic(int(payload))
        except Exception as e:
            print(e)
    if topic == "/addSimulatedCar":
        print("entrou", topic)
        payload = msg.payload
        addSimulatedCar(payload)

    if topic == "/endSimulation":
        print("Ending simulation...")
        endSimulation()
        print("Simulation ended")


if __name__ == "__main__":
    options = get_options()
    if options.nogui:
        sumoBinary = sumolib.checkBinary('sumo')
    else:
        sumoBinary = sumolib.checkBinary('sumo-gui')

    # Inicia a conexão MQTT
    mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_publish = on_publish
    mqtt_client.on_message = on_message
    mqtt_client.connect("localhost", 1883, 60)
    mqtt_client.subscribe("/realDatateste")
    mqtt_client.subscribe("/addRandomTraffic")
    mqtt_client.subscribe("/addSimulatedCar")
    mqtt_client.subscribe("/endSimulation")

    mqtt_client.loop_start()  # Inicia o loop de eventos MQTT em uma thread separada

    # Inicia o SUMO em uma thread separada

    # Aveiro sumo network
    sumo_thread = threading.Thread(target=traci.start, args=[
        [sumoBinary, "-c", "../Adapters/co_simulation/sumo_configuration/simple-map/simple-map.sumocfg",
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

    net = sumolib.net.readNet(
        "../Adapters/co_simulation/sumo_configuration/simple-map/simple-map.net.xml",withInternal=True)  # Carrega a rede do SUMO atraves do sumolib para acesso estatico

    #sumolib para dados estaticos da rede e traci para dados dinamicos da simulação
    print(type(net.getEdge("-1545").getType()))
    #teste = net.getEdge("-1545").getLanes()
    #for i in teste:
    #    print(i.getPermissions())

    run()
