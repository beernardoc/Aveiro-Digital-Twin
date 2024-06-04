# PI_Digital_Twin
Project for the Project in Informatics class

## Team

| Name           | **Email**            | NMEC   
| -------------  | -------------------- | ----- 
| Bernardo Pinto | bernardopinto@ua.pt  | 105926
| Filipe Obrist  | filipe.obrist@ua.pt  | 107471 
| Mariana Perna  | marianaperna@ua.pt   | 108067
| José Mendes    | mendes.j@ua.pt       | 107188
| Rafaela Dias   | rafaelasdias@ua.pt   | 108782

## How to run

Inside the DigitalTwin directory

```bash
./run.sh
```

> While running, the API documentation is available on the endpoint: http://localhost:5000/swagger

## Obtain Graphs

To obtain graphs comparing 2 simulations that have been saved, go to the directory `DigitalTwin/backend`
and run:

```bash
python3 results/compare_traffic.py {saved_sim_name1} {saved_sim_name2}
```

The graphs will appear in the `DigitalTwin/generated_graphs` directory 

## Export a new map

- Generated the .osm file through https://www.openstreetmap.org/

- Polished the mapping, removing unwanted parts with JOSM

- Deleted the 'delete' actions from the .osm file

```
osmfilter *in*.osm --drop-tags="@action='delete'" -o=*out*.osm
```

- using Adapters/co_simulation/map_adjustor/osm_to_xodr/main.py
    - Generate the header to the xodr file
    - Generate a new .osm file to transform to .xodr (map_modified_for_Carla.osm)
    
- using Adapters/co_simulation/map_adjustor/osm_to_xodr/converter.py create the .xodr file for CARLA (map_modified_for_Carla.osm as a parameter inside converter.py ) ***

- Through the .xodr file, we can generate the network (.net.xml) file for SUMO
```
python3 Adapters/co_simulation/map_adjustor/xodr_to_netxml/netconvert_carla.py --output *out*.net.xml --guess-tls ~/Desktop/PI_Digital_Twin/Adapters/co_simulation/sumo_configuration/simple-map/*in*.xodr 
```

- Change the .sumocfg with the desired inputs
