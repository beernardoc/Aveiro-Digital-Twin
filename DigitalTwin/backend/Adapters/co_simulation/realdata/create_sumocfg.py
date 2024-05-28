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




class RealData:
    def __init__(self, start_time, input_data):  #, input_data):
        self.start_time = start_time
        self.input_data = input_data
        self.base_file = "Adapters/co_simulation/realdata/base_file.xml"
        self.tree = ET.parse(self.base_file)
        self.root = self.tree.getroot()
        self.temp_file = io.StringIO()
        self.output_file = "Adapters/co_simulation/sumo_configuration/simple-map/realdata.rou.xml"
        self.tree.write(self.output_file)
        self.known_vehicle = {}



    def json_converter(self):  #converter o valor do json que vem como parametro, se estiver errado
        print(self.input_data[0]["value"][0]["entityId"])
        data = json.loads(self.input_data[0]["value"])
        print(data)
        return ""

    def iterate_data(self):

        for data in self.input_data[0]["value"]:
            vehicle_id = data["entityId"].split(":")[-1]


            if data["attrName"] == "observedBy" and "Radar" in data["attrValue"] and vehicle_id not in self.known_vehicle:
                self.known_vehicle[vehicle_id] = {}
                self.known_vehicle[vehicle_id]["observedBy"] = "p" + data["attrValue"].split(":")[-1][1:]
                self.known_vehicle[vehicle_id]["recvTime"] = data["recvTime"]


            if(vehicle_id in self.known_vehicle):

                if data["attrName"] == "heading" and "heading" not in self.known_vehicle[vehicle_id]:
                    print("entrou")
                    self.known_vehicle[vehicle_id]["heading"] = data["attrValue"]

                if data["attrName"] == "location" and "location" not in self.known_vehicle[vehicle_id]:
                    self.known_vehicle[vehicle_id]["location"] = [data["attrValue"]["coordinates"][1],
                                                                  data["attrValue"]["coordinates"][0]]

                if data["attrName"] == "speed" and "speed" not in self.known_vehicle[vehicle_id]:
                    # data["attrValue"] is in m/s, we need to convert it to km/h
                    speed_kmh = data["attrValue"] * 3.6
                    self.known_vehicle[vehicle_id]["speed"] = speed_kmh








        print(self.known_vehicle)



    def get_route(self, vehicle_id):
        try:
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
        except Exception as e:
            print(e)
            return

    def create_vehicle(self, vehicle_id):
        route = self.get_route(vehicle_id)
        if route is None:
            return

        vehicle = ET.SubElement(self.root, "vehicle")
        vehicle.set("id", "realdata_" + vehicle_id)
        vehicle.set("depart", self.calculate_depart_time(self.known_vehicle[vehicle_id]["recvTime"]))
        vehicle.set("departLane", "best")
        vehicle.set("departSpeed", "1")
        vehicle.set("type", "vehicle.ford.mustang")
        vehicle.set("color", "1,0,0") 

    def create_vehicle_route(self, vehicle_id):
        route = self.get_route(vehicle_id)
        if route is None:
            return

        # route must be inside the vehicle element
        vehicle = self.root.find("vehicle[@id='realdata_" + vehicle_id + "']")
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

    def calculate_depart_time(self, recv_time):
        format = "%Y-%m-%dT%H:%M:%S.%fZ"
        print(recv_time, self.start_time)

        start_dt = datetime.strptime(self.start_time, format)
        recv_dt = datetime.strptime(recv_time, format)

        # Calcular a diferença em segundos
        time_difference = (recv_dt - start_dt).total_seconds()

        return str(time_difference)
