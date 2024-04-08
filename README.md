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

- Install requirements
```bash
pip install -r requirements.txt
```

- Run carla server
```bash
./CarlaUE4.sh
```

- Load map
```bash
python3 config.py -x ~/Desktop/PI_Digital_Twin/Adapters/co_simulation/sumo_configuration/output.xodr
```

- Run co-simulation
```bash
 python3 main.py sumo_configuration/ruadapega.sumocfg --tls-manager carla --sumo-gui
```


## Export map

- Gera o .osm

- utiliza netconvert --osm-files simple-map.osm -o simple-map.net.xml para gerar o .net.xml para o sumo

- com Adapters/co_simulation/map_adjustor/converter.py crio o xodr para o carla

- com Adapters/co_simulation/map_adjustor/main.py crio um novo header para o xodr e altero manualmente




