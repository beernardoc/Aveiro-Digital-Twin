import json
import os
import sys
import optparse
import threading
import time

from sumolib import checkBinary
import traci
import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print(f"Conectado ao broker com código de resultado {rc}")


def on_publish(client, userdata, mid):
    print(f"Mensagem publicada com sucesso")


def on_message(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")


if __name__ == "__main__":
    # Inicia a conexão MQTT
    mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_publish = on_publish
    mqtt_client.on_message = on_message
    mqtt_client.connect("localhost", 1883, 60)
    mqtt_client.loop_start()  # Inicia o loop de eventos MQTT em uma thread separada

    coordenadas = [
        {"lat": 40.6361250091032, "lng": -8.659596064875444},
        {"lat": 40.63614421690061, "lng": -8.659584022192302},
        {"lat": 40.63617451402699, "lng": -8.659565026833864},
        {"lat": 40.63621796381109, "lng": -8.659537747677366},
        {"lat": 40.636280362615636, "lng": -8.6594983934419},
        {"lat": 40.63635442498533, "lng": -8.659451569633564},
        {"lat": 40.636445762348984, "lng": -8.65939350430772},
        {"lat": 40.636548697617705, "lng": -8.659328563126143},
        {"lat": 40.636663397520344, "lng": -8.659257355031114},
        {"lat": 40.63677383776296, "lng": -8.659189109605107},
        {"lat": 40.63688392296575, "lng": -8.659121026816775},
        {"lat": 40.636996428455866, "lng": -8.659051446928977},
        {"lat": 40.637109249752726, "lng": -8.65898167146447},
        {"lat": 40.63722340802476, "lng": -8.658911068865555},
        {"lat": 40.637333804417715, "lng": -8.658842792590345},
        {"lat": 40.637449686271246, "lng": -8.658771123479337},
        {"lat": 40.63756888953621, "lng": -8.658697399894125},
        {"lat": 40.63828, "lng": -8.657928} # Final

    ]

    simple_coordenadas = [
        {"lat": 40.62933483119786, "lng": -8.66010201239263},
        {"lat": 40.62935257287997, "lng": -8.660101040327385},
        {"lat": 40.62938677784761, "lng": -8.660099166238671},
        {"lat": 40.62944368215245, "lng": -8.660098676542598},
        {"lat": 40.6295127794496, "lng": -8.660108871498423},
        {"lat": 40.629594589800035, "lng": -8.66013502761367},
        {"lat": 40.62969499748144, "lng": -8.66017064273069},
        {"lat": 40.629790483589424, "lng": -8.660259508972047},
        {"lat": 40.62988541589939, "lng": -8.660362736356399},
        {"lat": 40.62997934150819, "lng": -8.660464957817915},
        {"lat": 40.63007770924723, "lng": -8.660572014169281},
        {"lat": 40.630172762051735, "lng": -8.66067546318784},
        {"lat": 40.63026892659765, "lng": -8.660780122553154},
        {"lat": 40.63036520035903, "lng": -8.66088490118757},
        {"lat": 40.63046536270231, "lng": -8.66099391235428},
        {"lat": 40.630565201591715, "lng": -8.661102571929169},
        {"lat": 40.63066420578726, "lng": -8.661210323496995},
        {"lat": 40.63076177185798, "lng": -8.661316510296796},
        {"lat": 40.630867704240984, "lng": -8.661415672312303},
        {"lat": 40.63097951349384, "lng": -8.661506349395134},
        {"lat": 40.631091477246535, "lng": -8.66159715213976},
        {"lat": 40.63120451034948, "lng": -8.661679352315968},
        {"lat": 40.63132213568331, "lng": -8.66173693627149},
        {"lat": 40.63144462149907, "lng": -8.661791294693783},
        {"lat": 40.63156123488296, "lng": -8.661842885844951},
        {"lat": 40.63168203450969, "lng": -8.661871153306807},
        {"lat": 40.63180747280031, "lng": -8.661897108416104},
        {"lat": 40.631928498262006, "lng": -8.661905871574694},
        {"lat": 40.63205308993659, "lng": -8.66189742653129},
        {"lat": 40.63218451096426, "lng": -8.661874813303315},
        {"lat": 40.63230528141712, "lng": -8.661832984760643},
        {"lat": 40.63243306439414, "lng": -8.661788238732635},
        {"lat": 40.632551820140435, "lng": -8.66172878497674},
        {"lat": 40.63266966489623, "lng": -8.661662175539563},
        {"lat": 40.63278579484792, "lng": -8.661596535110075},
        {"lat": 40.632897949618545, "lng": -8.661533141345165},
        {"lat": 40.63300930844198, "lng": -8.661470197246638},
        {"lat": 40.63312662962101, "lng": -8.661403882757115}
    ]

    real = [
                {'lat': 40.63500948679511, 'lng': -8.660327237409504, 'heading': 154.70},
                {'lat': 40.635002764957555, 'lng': -8.660330072663871, 'heading': 154.70},
                {'lat': 40.63499497628642, 'lng': -8.660334161664197, 'heading': 154.70},
                {'lat': 40.634989561909535, 'lng': -8.660339258588648, 'heading': 154.70},
                {'lat': 40.63498382669651, 'lng': -8.660339668291709, 'heading': 154.70},
                {'lat': 40.63497963957126, 'lng': -8.660345855080894, 'heading': 154.70},
                {'lat': 40.63497414498534, 'lng': -8.660349780199997, 'heading': 154.70},
                {'lat': 40.63496750335681, 'lng': -8.66035378725971, 'heading': 154.70},
                {'lat': 40.63496192856186, 'lng': -8.660356540573467, 'heading': 154.70},
                {'lat': 40.63495643397594, 'lng': -8.66036046569257, 'heading': 154.70}
            ]
    
    real2 = [
        {'lat': 40.63549469474595, 'lng': -8.660006434840769}
    ]


    # For Aveiro Map
    # for coordenada in coordenadas:

    #     data = {
    #         "vehicle": "VEICULOTEST",
    #         "data": {
    #             "location": {
    #                 "lat": coordenada["lat"],
    #                 "lng": coordenada["lng"]
    #             },
    #             "speed": 43
    #         }
    #     }

    realreal = [
{'acceleration': 0.15270089711777002,
 'classification': 5,
 'cloudPersist': True,
 'confidence': 100,
 'heading': -25.311,
 'latitude': 40.635271093252236,
 'length': 4.6000000000000005,
 'longitude': -8.660141339184497,
 'objectID': 1015,
 'receiverID': 1,
 'speed': 10.5,
 'test': {},
 'timestamp': 1710954012.654875},


{'acceleration': 0.0,
 'classification': 5,
 'cloudPersist': False,
 'confidence': 100,
 'heading': -25.311,
 'latitude': 40.63527781508979,
 'length': 5.6000000000000005,
 'longitude': -8.66013850393013,
 'objectID': 1015,
 'receiverID': 1,
 'speed': 10.5,
 'test': {},
 'timestamp': 1710954012.729859},


{'acceleration': 0.12423687499534289,
 'classification': 5,
 'cloudPersist': False,
 'confidence': 100,
 'heading': -25.311,
 'latitude': 40.635284456718324,
 'length': 5.6000000000000005,
 'longitude': -8.660134496870414,
 'objectID': 1015,
 'receiverID': 1,
 'speed': 10.600000000000001,
 'test': {},
 'timestamp': 1710954012.804914},


{'acceleration': 0.0,
 'classification': 5,
 'cloudPersist': False,
 'confidence': 100,
 'heading': -25.311,
 'latitude': 40.635289951304244,
 'length': 5.6000000000000005,
 'longitude': -8.660130571751312,
 'objectID': 1015,
 'receiverID': 1,
 'speed': 10.600000000000001,
 'test': {},
 'timestamp': 1710954012.879831},


{'acceleration': 0.10472925915569328,
 'classification': 5,
 'cloudPersist': True,
 'confidence': 100,
 'heading': -25.311,
 'latitude': 40.63529536568113,
 'length': 5.6000000000000005,
 'longitude': -8.660125474826861,
 'objectID': 1015,
 'receiverID': 1,
 'speed': 10.700000000000001,
 'test': {},
 'timestamp': 1710954012.954843},


{'acceleration': 0.0,
 'classification': 5,
 'cloudPersist': False,
 'confidence': 100,
 'heading': -25.311,
 'latitude': 40.63530192710063,
 'length': 5.6000000000000005,
 'longitude': -8.6601202959618,
 'objectID': 1015,
 'receiverID': 1,
 'speed': 10.700000000000001,
 'test': {},
 'timestamp': 1710954013.02986},


{'acceleration': 0.0,
 'classification': 5,
 'cloudPersist': False,
 'confidence': 100,
 'heading': -25.311,
 'latitude': 40.63530750189558,
 'length': 5.6000000000000005,
 'longitude': -8.660117542648045,
 'objectID': 1015,
 'receiverID': 1,
 'speed': 10.700000000000001,
 'test': {},
 'timestamp': 1710954013.104894},


{'acceleration': 0.5537067901063651,
 'classification': 5,
 'cloudPersist': False,
 'confidence': 100,
 'heading': -25.311,
 'latitude': 40.63531422373314,
 'length': 5.6000000000000005,
 'longitude': -8.660114707393678,
 'objectID': 1015,
 'receiverID': 1,
 'speed': 10.8,
 'test': {},
 'timestamp': 1710954013.180601},


{'acceleration': 0.39263880763446757,
 'classification': 5,
 'cloudPersist': True,
 'confidence': 100,
 'heading': -25.311,
 'latitude': 40.63532086536166,
 'length': 5.6000000000000005,
 'longitude': -8.660110700333963,
 'objectID': 1015,
 'receiverID': 1,
 'speed': 10.9,
 'test': {},
 'timestamp': 1710954013.254687},


{'acceleration': 0.0,
 'classification': 5,
 'cloudPersist': False,
 'confidence': 100,
 'heading': -25.311,
 'latitude': 40.635327506990194,
 'length': 5.6000000000000005,
 'longitude': -8.660106693274248,
 'objectID': 1015,
 'receiverID': 1,
 'speed': 10.9,
 'test': {},
 'timestamp': 1710954013.329629}


    ]


    # For Simple Map
    for coordenada in realreal:
        data = {
            "vehicle": str(coordenada["objectID"]),
            "data": {
                "location": {
                    "lat": coordenada["latitude"],
                    "lng": coordenada["longitude"]
                },
                "heading": coordenada["heading"],
                "speed": coordenada["speed"]
            }
        }

        payload = json.dumps(data)
        mqtt_client.publish("/teste", payload)
        time.sleep(0.8)
