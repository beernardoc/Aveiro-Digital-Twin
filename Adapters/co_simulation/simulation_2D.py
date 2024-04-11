import json
import os
import random
import sys
import optparse
import threading
import time

import sumolib

import traci
import paho.mqtt.client as mqtt
from flask import logging


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
        #if len(lista) > 0:
        #    for key in lista.keys():
        #        addOrUpdateCar({"vehicle": key, "data": lista[
        #           key]})  # para nao desregular os steps do sumo, a função addOrUpdateCar é chamada aqui

        traci.simulationStep()


        step += 1


    traci.close()
    sys.stdout.flush()


def addOrUpdateCar(received):
    log, lat = received["data"]["location"]["lng"], received["data"]["location"]["lat"]
    vehID = received["vehicle"]
    x, y = traci.simulation.convertGeo(log, lat, True)
    nextEdge = traci.simulation.convertRoad(log, lat, True)[
        0]  # calcula a proxima aresta que o veículo vai passar de acordo com as coordenadas recebidas
    allCars = traci.vehicle.getIDList()
    print("next", nextEdge)

    if vehID in allCars:  # Verifica se o veículo já existe
        print(traci.vehicle.getRoadID(vehID))
        if traci.vehicle.getRoadID(vehID) == nextEdge or nextEdge.startswith(":cluster") or "_" in nextEdge:
            traci.vehicle.moveToXY(vehID, nextEdge, 0, x, y,
                                   keepRoute=1)  # se a proxima for a mesma, cluster ou de junção, move com moveTOXY


        else:
            traci.vehicle.changeTarget(vehID, nextEdge)  # se a proxima aresta for diferente, muda a rota
            print("mudou", traci.vehicle.getRoute(vehID))


    else:  # Adiciona um novo veículo
        traci.route.add(routeID=("route_" + vehID), edges=[nextEdge])  # adiciona uma rota para o veículo
        print("definiu rota")
        traci.vehicle.add(vehID, routeID=("route_" + vehID), typeID="vehicle.audi.a2", depart="now", departSpeed=0,
                          departLane="best", )
        print(traci.vehicle.getRoute(vehID))
        print("aq", traci.vehicle.getRoadID(vehID))
        print("adicionado")


def addRandomTraffic(QtdCars):
    allowedEdges = [i.getID() for i in net.getEdges() for j in i.getLanes() if "passenger" in j.getPermissions()]

    if len(allowedEdges) != 0:

        for count in range(QtdCars):
            routeID = "route_{}".format(time.time_ns())
            vehicle_id = "sumo_{}".format(time.time_ns())
            route = traci.simulation.findRoute(random.choice(allowedEdges), random.choice(allowedEdges), vType="vehicle.audi.a2")
            if route.edges:
                traci.route.add(routeID, route.edges)
                traci.vehicle.add(vehicle_id, routeID, typeID="vehicle.audi.a2", depart="now", departSpeed=0,
                              departLane="best", )


def on_connect(client, userdata, flags, rc):
    print(f"Conectado ao broker com código de resultado {rc}")


def on_publish(client, userdata, mid):
    print("Mensagem publicada com sucesso")


def on_message(client, userdata, msg):
    topic = msg.topic
    print(topic)
    if topic == "/teste":
        payload = json.loads(msg.payload)
        lista[payload["vehicle"]] = payload["data"]
        print(lista)
    if topic == "/addRandomTraffic":
        payload = json.loads(msg.payload)
        try:
            addRandomTraffic(int(payload))
        except Exception as e:
            print(e)


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
    mqtt_client.subscribe("/teste")
    mqtt_client.subscribe("/addRandomTraffic")
    mqtt_client.loop_start()  # Inicia o loop de eventos MQTT em uma thread separada

    # Inicia o SUMO em uma thread separada

    # Aveiro sumo network
    sumo_thread = threading.Thread(target=traci.start, args=[
        [sumoBinary, "-c", "../Adapters/co_simulation/sumo_configuration/simple-map/simple-map.sumocfg",
         "--tripinfo-output",
         "tripinfo.xml"]])

    # Simple sumo network
    # sumo_thread = threading.Thread(target=traci.start, args=[
    #     [sumoBinary, "-c", "../simple_sumo_network/osm.sumocfg", "--tripinfo-output", "simple_tripinfo.xml"]])
    sumo_thread.start()
    # Executa a função run (controle do SUMO) após o início do SUMO
    sumo_thread.join()  # Aguarda até que o SUMO esteja pronto

    net = sumolib.net.readNet(
        "../Adapters/co_simulation/sumo_configuration/simple-map/simple-map.net.xml")  # Carrega a rede do SUMO atraves do sumolib para acesso estatico

    #sumolib para dados estaticos da rede e traci para dados dinamicos da simulação

    #teste = net.getEdge("-1545").getLanes()
    #for i in teste:
    #    print(i.getPermissions())

    run()
