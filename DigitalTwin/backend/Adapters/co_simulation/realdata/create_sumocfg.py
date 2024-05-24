import io
import json
from math import atan2, cos, pi, radians, sin
import xml.etree.ElementTree as ET
from datetime import datetime
# import rtree
import pyproj
import sumolib
import os

radar_file_path = "Adapters/co_simulation/radar.json"


json_data = {
  "type": "StructuredValue",
  "value": [
    {
      "_id": "664b60403eb16b14b485e640",
      "entityId": "urn:ngsi-ld:Car:554123756",
      "entityType": "Car",
      "attrName": "detectedID",
      "attrType": "Text",
      "attrValue": 554123756,
      "recvTime": "2024-05-20T14:37:52.772Z"
    },
    {
      "_id": "664b60403eb16b14b485e647",
      "entityId": "urn:ngsi-ld:Car:554123756",
      "entityType": "Car",
      "attrName": "hasDevices",
      "attrType": "Array",
      "attrValue": [],
      "recvTime": "2024-05-20T14:37:52.772Z"
    },
    {
      "_id": "664b60403eb16b14b485e642",
      "entityId": "urn:ngsi-ld:Car:554123756",
      "entityType": "Car",
      "attrName": "heading",
      "attrType": "Float",
      "attrValue": -162.132,
      "recvTime": "2024-05-20T14:37:52.772Z"
    },
    {
      "_id": "664b60403eb16b14b485e644",
      "entityId": "urn:ngsi-ld:Car:554123756",
      "entityType": "Car",
      "attrName": "length",
      "attrType": "Float",
      "attrValue": 5.6,
      "recvTime": "2024-05-20T14:37:52.772Z"
    },
    {
      "_id": "664b60403eb16b14b485e645",
      "entityId": "urn:ngsi-ld:Car:554123756",
      "entityType": "Car",
      "attrName": "location",
      "attrType": "geo:json",
      "attrValue": {
        "type": "Point",
        "coordinates": [
          -8.648441571,
          40.632023698
        ]
      },
      "recvTime": "2024-05-20T14:37:52.772Z"
    },
    {
      "_id": "664b60403eb16b14b485e641",
      "entityId": "urn:ngsi-ld:Car:554123756",
      "entityType": "Car",
      "attrName": "observedBy",
      "attrType": "Relationship",
      "attrValue": "urn:ngsi-ld:SlpRadar:033",
      "recvTime": "2024-05-20T14:37:52.772Z"
    },
    {
      "_id": "664b60403eb16b14b485e646",
      "entityId": "urn:ngsi-ld:Car:554123756",
      "entityType": "Car",
      "attrName": "speed",
      "attrType": "Float",
      "attrValue": 3.4,
      "recvTime": "2024-05-20T14:37:52.772Z"
    },
    {
      "_id": "664b60401d12d30f3042bd73",
      "entityId": "urn:ngsi-ld:Car:554123756",
      "entityType": "Car",
      "attrName": "acceleration",
      "attrType": "Float",
      "attrValue": 1.635046681,
      "recvTime": "2024-05-20T14:37:52.843Z"
    },
    {
      "_id": "664b60401d12d30f3042bd77",
      "entityId": "urn:ngsi-ld:Car:554123756",
      "entityType": "Car",
      "attrName": "confidence",
      "attrType": "Float",
      "attrValue": 100,
      "recvTime": "2024-05-20T14:37:52.843Z"
    },
    {
      "_id": "664b60401d12d30f3042bd74",
      "entityId": "urn:ngsi-ld:Car:554123756",
      "entityType": "Car",
      "attrName": "detectedID",
      "attrType": "Text",
      "attrValue": 554123756,
      "recvTime": "2024-05-20T14:37:52.843Z"
    },
    {
      "_id": "664b60401d12d30f3042bd7b",
      "entityId": "urn:ngsi-ld:Car:554123756",
      "entityType": "Car",
      "attrName": "hasDevices",
      "attrType": "Array",
      "attrValue": [],
      "recvTime": "2024-05-20T14:37:52.843Z"
    },
    {
      "_id": "664b60401d12d30f3042bd76",
      "entityId": "urn:ngsi-ld:Car:554123756",
      "entityType": "Car",
      "attrName": "heading",
      "attrType": "Float",
      "attrValue": -162.132,
      "recvTime": "2024-05-20T14:37:52.843Z"
    },
    {
      "_id": "664b60401d12d30f3042bd78",
      "entityId": "urn:ngsi-ld:Car:554123756",
      "entityType": "Car",
      "attrName": "length",
      "attrType": "Float",
      "attrValue": 5.6,
      "recvTime": "2024-05-20T14:37:52.843Z"
    },
    {
      "_id": "664b60401d12d30f3042bd79",
      "entityId": "urn:ngsi-ld:Car:554123756",
      "entityType": "Car",
      "attrName": "location",
      "attrType": "geo:json",
      "attrValue": {
        "type": "Point",
        "coordinates": [
          -8.64844127,
          40.632020261
        ]
      },
      "recvTime": "2024-05-20T14:37:52.843Z"
    },
    {
      "_id": "664b60401d12d30f3042bd75",
      "entityId": "urn:ngsi-ld:Car:554123756",
      "entityType": "Car",
      "attrName": "observedBy",
      "attrType": "Relationship",
      "attrValue": "urn:ngsi-ld:SlpRadar:033",
      "recvTime": "2024-05-20T14:37:52.843Z"
    },
    {
      "_id": "664b60401d12d30f3042bd7a",
      "entityId": "urn:ngsi-ld:Car:554123756",
      "entityType": "Car",
      "attrName": "speed",
      "attrType": "Float",
      "attrValue": 3.7,
      "recvTime": "2024-05-20T14:37:52.843Z"
    },
    {
      "_id": "664b60401d12d30f3042bd7c",
      "entityId": "urn:ngsi-ld:Car:554123756",
      "entityType": "Car",
      "attrName": "acceleration",
      "attrType": "Float",
      "attrValue": -0.381161475,
      "recvTime": "2024-05-20T14:37:52.914Z"
    },
    {
      "_id": "664b60401d12d30f3042bd80",
      "entityId": "urn:ngsi-ld:Car:554123756",
      "entityType": "Car",
      "attrName": "confidence",
      "attrType": "Float",
      "attrValue": 100,
      "recvTime": "2024-05-20T14:37:52.914Z"
    },
    {
      "_id": "664b60401d12d30f3042bd7d",
      "entityId": "urn:ngsi-ld:Car:554123756",
      "entityType": "Car",
      "attrName": "detectedID",
      "attrType": "Text",
      "attrValue": 554123756,
      "recvTime": "2024-05-20T14:37:52.914Z"
    },
    {
      "_id": "664b60401d12d30f3042bd84",
      "entityId": "urn:ngsi-ld:Car:554123756",
      "entityType": "Car",
      "attrName": "hasDevices",
      "attrType": "Array",
      "attrValue": [],
      "recvTime": "2024-05-20T14:37:52.914Z"
    },
    {
      "_id": "664b60401d12d30f3042bd7f",
      "entityId": "urn:ngsi-ld:Car:554123756",
      "entityType": "Car",
      "attrName": "heading",
      "attrType": "Float",
      "attrValue": -157.53,
      "recvTime": "2024-05-20T14:37:52.914Z"
    },
    {
      "_id": "664b60401d12d30f3042bd81",
      "entityId": "urn:ngsi-ld:Car:554123756",
      "entityType": "Car",
      "attrName": "length",
      "attrType": "Float",
      "attrValue": 5.6,
      "recvTime": "2024-05-20T14:37:52.914Z"
    },
    {
      "_id": "664b60401d12d30f3042bd82",
      "entityId": "urn:ngsi-ld:Car:554123756",
      "entityType": "Car",
      "attrName": "location",
      "attrType": "geo:json",
      "attrValue": {
        "type": "Point",
        "coordinates": [
          -8.648434144,
          40.632019704
        ]
      },
      "recvTime": "2024-05-20T14:37:52.914Z"
    },
    {
      "_id": "664b60401d12d30f3042bd7e",
      "entityId": "urn:ngsi-ld:Car:554123756",
      "entityType": "Car",
      "attrName": "observedBy",
      "attrType": "Relationship",
      "attrValue": "urn:ngsi-ld:SlpRadar:033",
      "recvTime": "2024-05-20T14:37:52.914Z"
    },
    {
      "_id": "664b60401d12d30f3042bd83",
      "entityId": "urn:ngsi-ld:Car:554123756",
      "entityType": "Car",
      "attrName": "speed",
      "attrType": "Float",
      "attrValue": 3.6,
      "recvTime": "2024-05-20T14:37:52.914Z"
    },
    {
      "_id": "664b60401d12d30f3042bd85",
      "entityId": "urn:ngsi-ld:Car:554123756",
      "entityType": "Car",
      "attrName": "acceleration",
      "attrType": "Float",
      "attrValue": 0.29093956,
      "recvTime": "2024-05-20T14:37:52.994Z"
    },
    {
      "_id": "664b60401d12d30f3042bd89",
      "entityId": "urn:ngsi-ld:Car:554123756",
      "entityType": "Car",
      "attrName": "confidence",
      "attrType": "Float",
      "attrValue": 100,
      "recvTime": "2024-05-20T14:37:52.994Z"
    },
    {
      "_id": "664b60401d12d30f3042bd86",
      "entityId": "urn:ngsi-ld:Car:554123756",
      "entityType": "Car",
      "attrName": "detectedID",
      "attrType": "Text",
      "attrValue": 554123756,
      "recvTime": "2024-05-20T14:37:52.994Z"
    },
    {
      "_id": "664b60401d12d30f3042bd8d",
      "entityId": "urn:ngsi-ld:Car:554123756",
      "entityType": "Car",
      "attrName": "hasDevices",
      "attrType": "Array",
      "attrValue": [],
      "recvTime": "2024-05-20T14:37:52.994Z"
    },
    {
      "_id": "664b60401d12d30f3042bd88",
      "entityId": "urn:ngsi-ld:Car:554123756",
      "entityType": "Car",
      "attrName": "heading",
      "attrType": "Float",
      "attrValue": -158.769,
      "recvTime": "2024-05-20T14:37:52.994Z"
    },
    {
      "_id": "664b60401d12d30f3042bd8a",
      "entityId": "urn:ngsi-ld:Car:554123756",
      "entityType": "Car",
      "attrName": "length",
      "attrType": "Float",
      "attrValue": 5.6,
      "recvTime": "2024-05-20T14:37:52.994Z"
    },
    {
      "_id": "664b60401d12d30f3042bd8b",
      "entityId": "urn:ngsi-ld:Car:554123756",
      "entityType": "Car",
      "attrName": "location",
      "attrType": "geo:json",
      "attrValue": {
        "type": "Point",
        "coordinates": [
          -8.648435114,
          40.632017315
        ]
      },
      "recvTime": "2024-05-20T14:37:52.994Z"
    },
    {
      "_id": "664b60401d12d30f3042bd87",
      "entityId": "urn:ngsi-ld:Car:554123756",
      "entityType": "Car",
      "attrName": "observedBy",
      "attrType": "Relationship",
      "attrValue": "urn:ngsi-ld:SlpRadar:033",
      "recvTime": "2024-05-20T14:37:52.994Z"
    },
    {
      "_id": "664b60401d12d30f3042bd8c",
      "entityId": "urn:ngsi-ld:Car:554123756",
      "entityType": "Car",
      "attrName": "speed",
      "attrType": "Float",
      "attrValue": 3.7,
      "recvTime": "2024-05-20T14:37:52.994Z"
    },
    {
      "_id": "664b60411d12d30f3042bd8e",
      "entityId": "urn:ngsi-ld:Car:554123756",
      "entityType": "Car",
      "attrName": "acceleration",
      "attrType": "Float",
      "attrValue": -0.462776567,
      "recvTime": "2024-05-20T14:37:53.071Z"
    },
    {
      "_id": "664b60411d12d30f3042bd92",
      "entityId": "urn:ngsi-ld:Car:554123756",
      "entityType": "Car",
      "attrName": "confidence",
      "attrType": "Float",
      "attrValue": 100,
      "recvTime": "2024-05-20T14:37:53.071Z"
    },
    {
      "_id": "664b60411d12d30f3042bd8f",
      "entityId": "urn:ngsi-ld:Car:554123756",
      "entityType": "Car",
      "attrName": "detectedID",
      "attrType": "Text",
      "attrValue": 554123756,
      "recvTime": "2024-05-20T14:37:53.071Z"
    },
    {
      "_id": "664b60411d12d30f3042bd96",
      "entityId": "urn:ngsi-ld:Car:554123756",
      "entityType": "Car",
      "attrName": "hasDevices",
      "attrType": "Array",
      "attrValue": [],
      "recvTime": "2024-05-20T14:37:53.071Z"
    },
    {
      "_id": "664b60411d12d30f3042bd91",
      "entityId": "urn:ngsi-ld:Car:554123756",
      "entityType": "Car",
      "attrName": "heading",
      "attrType": "Float",
      "attrValue": -155.406,
      "recvTime": "2024-05-20T14:37:53.071Z"
    },
    {
      "_id": "664b60411d12d30f3042bd93",
      "entityId": "urn:ngsi-ld:Car:554123756",
      "entityType": "Car",
      "attrName": "length",
      "attrType": "Float",
      "attrValue": 5.6,
      "recvTime": "2024-05-20T14:37:53.071Z"
    },
    {
      "_id": "664b60411d12d30f3042bd94",
      "entityId": "urn:ngsi-ld:Car:554123756",
      "entityType": "Car",
      "attrName": "location",
      "attrType": "geo:json",
      "attrValue": {
        "type": "Point",
        "coordinates": [
          -8.64843033,
          40.632016562
        ]
      },
      "recvTime": "2024-05-20T14:37:53.071Z"
    },
    {
      "_id": "664b60411d12d30f3042bd90",
      "entityId": "urn:ngsi-ld:Car:554123756",
      "entityType": "Car",
      "attrName": "observedBy",
      "attrType": "Relationship",
      "attrValue": "urn:ngsi-ld:SlpRadar:033",
      "recvTime": "2024-05-20T14:37:53.071Z"
    },
    {
      "_id": "664b60411d12d30f3042bd95",
      "entityId": "urn:ngsi-ld:Car:554123756",
      "entityType": "Car",
      "attrName": "speed",
      "attrType": "Float",
      "attrValue": 3.5,
      "recvTime": "2024-05-20T14:37:53.071Z"
    }
  ]
}

json_data = json.dumps(json_data)



class Livedata:
    def __init__(self, start_time): #, input_data):
        self.start_time = start_time
        self.input_data = json_data
        self.base_file = "Adapters/co_simulation/livedata/base_file.xml"
        self.tree = ET.parse(self.base_file)
        self.root = self.tree.getroot()
        self.temp_file = io.StringIO()
        self.output_file = "Adapters/co_simulation/sumo_configuration/simple-map/realdata.rou.xml"
        self.tree.write(self.output_file)
        self.known_vehicle = {}

    def json_converter(self): #converter o valor do json que vem como parametro, se estiver errado

        data =  json.loads(self.input_data)
        #print(data["value"])
        return data["value"]

    def iterate_data(self):

        for data in self.json_converter():

            vehicle_id = data["entityId"].split(":")[-1]

            if data["attrName"] == "detectedID" and vehicle_id not in self.known_vehicle.keys():
                  self.known_vehicle[vehicle_id] = {}

            elif data["attrName"] == "heading" and "heading" not in self.known_vehicle[vehicle_id]:
                print("entrou")
                self.known_vehicle[vehicle_id]["heading"] = data["attrValue"]

            elif data["attrName"] == "location" and "location" not in self.known_vehicle[vehicle_id]:
                self.known_vehicle[vehicle_id]["location"] = [data["attrValue"]["coordinates"][1], data["attrValue"]["coordinates"][0]]

            elif data["attrName"] == "observedBy" and "observedBy" not in self.known_vehicle[vehicle_id]:
                self.known_vehicle[vehicle_id]["observedBy"] = "p" + data["attrValue"].split(":")[-1][1:]

            elif data["attrName"] == "speed" and "speed" not in self.known_vehicle[vehicle_id]:
                # data["attrValue"] is in m/s, we need to convert it to km/h
                speed_kmh = data["attrValue"] * 3.6
                self.known_vehicle[vehicle_id]["speed"] = speed_kmh


        print(self.known_vehicle)

    def get_route(self, vehicle_id):
      with open(radar_file_path, "r") as f:
        data = json.load(f)
        radar = None
        for r in data:
            if r["id"] == self.known_vehicle[vehicle_id]["observedBy"]:
                radar = r

        if radar is None:
            return

        radar_location = [radar["coord"]["lat"], radar["coord"]["lng"]]
        vehicle_location = self.known_vehicle[vehicle_id]["location"]

        angle = self.calculate_bearing(radar_location, vehicle_location)
        heading = self.known_vehicle[vehicle_id]["heading"]

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

        else:
            return

        return route

    def create_vehicle(self, vehicle_id):
        route = self.get_route(vehicle_id)
        if route is None:
            return

        vehicle = ET.SubElement(self.root, "vehicle")
        vehicle.set("id", "livedata_" + vehicle_id)
        vehicle.set("departLane", "best")
        vehicle.set("departSpeed", str(self.known_vehicle[vehicle_id]["speed"]))
        vehicle.set("type", "vehicle.dodge.charger_police_2020")
        vehicle.set("color", "1,0,0") # red
        # depart missing TODO

    def create_vehicle_route(self, vehicle_id):
        route = self.get_route(vehicle_id)
        if route is None:
            return

        # route must be inside the vehicle element
        vehicle = self.root.find("vehicle[@id='livedata_" + vehicle_id + "']")
        vehicle_route = ET.SubElement(vehicle, "route")
        route = [str(r) for r in route]
        route = " ".join(route)
        vehicle_route.set("edges", route)


    def calculate_bearing(self, coord1, coord2):
      """
      Function to calculate the bearing between two
      coordinates (latitude, longitude) in degrees.

      Note:   0deg is the North
              90deg is the East
              180deg is the South
              270deg is the West.

      Angle Type '0':
          0deg - 90deg and 270deg - 360deg => The vehicle is moving in the North of the radar
          90deg - 180deg and 180deg - 270deg => The vehicle is moving in the South of the radar

      Angle Type '1':
          0deg - 180deg => The vehicle is moving in the East of the radar
          180deg - 360deg => The vehicle is moving in the West of the radar
      """

      lat1 = radians(coord1[0])
      lon1 = radians(coord1[1])
      lat2 = radians(coord2[0])
      lon2 = radians(coord2[1])

      dlon = lon2 - lon1

      y = sin(dlon) * cos(lat2)
      x = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dlon)

      return (atan2(y, x) * 180 / pi + 360) % 360





if __name__ == '__main__':
    start_time = "2024-05-20T14:37:52.772Z"
    livedata = Livedata(start_time)
    livedata.iterate_data()
    print(livedata.get_route("554123756"))
    livedata.create_vehicle("554123756")
    livedata.tree.write(livedata.output_file)
    livedata.create_vehicle_route("554123756")
    livedata.tree.write(livedata.output_file)