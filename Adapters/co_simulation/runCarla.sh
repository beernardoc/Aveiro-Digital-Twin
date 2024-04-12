#!/bin/bash
# Open two terminals
gnome-terminal -- ~/Desktop/CARLA_0.9.15/CarlaUE4.sh
sleep 15
echo "Carla is running"
gnome-terminal -- python3 ~/Desktop/CARLA_0.9.15/PythonAPI/util/config.py -x ~/Desktop/PI_Digital_Twin/Adapters/co_simulation/sumo_configuration/simple-map/map-clean.xodr
