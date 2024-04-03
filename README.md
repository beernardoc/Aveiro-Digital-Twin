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

