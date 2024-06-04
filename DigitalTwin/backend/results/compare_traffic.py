import sys
import json
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

def cars_per_edge(file):
    with open(file, 'r') as f:
        data = json.load(f)

    # Excluir chaves que começam com ":"
    relevant_data = {key: value for key, value in data.items() if not key.startswith(':')}

    return relevant_data

def generate_RoundaboutGraph(file1, file2, type):
    data1 = cars_per_edge(file1)
    data2 = cars_per_edge(file2)

    with open('Adapters/co_simulation/roundabout.json', 'r') as f:
        roundabout_data = json.load(f)

    results_before = {roundabout['id']: 0 for roundabout in roundabout_data}
    results_after = {roundabout['id']: 0 for roundabout in roundabout_data}

    for roundabout in roundabout_data:
        roundabout_edges = roundabout['edges']
        for edge in roundabout_edges:
            results_before[roundabout["id"]] += data1[str(edge)]
            results_after[roundabout["id"]] += data2[str(edge)]

    difference = {}
    for key in roundabout_data:
        value1 = results_before[key['id']]
        value2 = results_after[key['id']]
        difference[key['id']] = value2 - value1

    keys = list(difference.keys())
    values = list(difference.values())

    colors = ['orange' if v > 0 else 'blue' for v in values]

    bar_width = 0.5

    plt.figure(figsize=(10, 6))  # Increase the figure size

    plt.bar(keys, values, color=colors, width=bar_width)
    plt.xlabel('Roundabout Number')

    fig_name = ""
    name1 = file1.split("_edges")[0].split("/")[-1]
    name2 = file2.split("_edges")[0].split("/")[-1]

    total_cars1 = get_total_cars(file1.split("_edges")[0] + "_total_vehicles.json")
    total_cars2 = get_total_cars(file2.split("_edges")[0] + "_total_vehicles.json")
    total_time1 = get_total_time(file1.split("_edges")[0] + "_total_vehicles.json")
    total_time2 = get_total_time(file2.split("_edges")[0] + "_total_vehicles.json")

    if type == "co2":
        plt.ylabel('Average Difference in CO2 Emissions (mg)')
        plt.title(f'Average Difference in CO2 Emissions per roundabout,\n {name2} ({total_cars2} vehicles in {total_time2} seconds) vs {name1} ({total_cars1} vehicles in {total_time1} seconds)')
        fig_name = f'RoundAboutCO2_difference-{name1}-{name2}.png'

    elif type == "fuel":
        plt.ylabel('Average Difference in Fuel Consumption (ml)')
        plt.title(f'Average Difference in Fuel Consumption per roundabout,\n {name2} ({total_cars2} vehicles in {total_time2} seconds) vs {name1} ({total_cars1} vehicles in {total_time1} seconds)')
        fig_name = f'RoundAboutFuel_difference-{name1}-{name2}.png'

    elif type == "max":
        plt.ylabel('Difference in the Maximum Number of Vehicles')
        plt.title(f'Difference in the Maximum Number of Vehicles per roundabout,\n {name2} ({total_cars2} vehicles in {total_time2} seconds) vs {name1} ({total_cars1} vehicles in {total_time1} seconds)')
        fig_name = f'RoundAboutMax_difference-{name1}-{name2}.png'

    elif type == "total":
        plt.ylabel('Difference in the Total Number of Vehicles')
        plt.title(f'Difference in the Total Number of Vehicles per roundabout,\n {name2} ({total_cars2} vehicles in {total_time2} seconds) vs {name1} ({total_cars1} vehicles in {total_time1} seconds)')
        fig_name = f'RoundAboutTotal_difference-{name1}-{name2}.png'

    elif type == "waiting":
        plt.ylabel('Average Difference in the Accumulated Waiting Time (s)')
        plt.title(f'Average Difference in the Accumulated Waiting Time per roundabout,\n {name2} ({total_cars2} vehicles in {total_time2} seconds) vs {name1} ({total_cars1} vehicles in {total_time1} seconds)')
        fig_name = f'RoundAboutWaiting_difference-{name1}-{name2}.png'

    plt.legend(handles=[Patch(color='orange', label=f'{name2} > {name1}'), Patch(color='blue', label=f'{name1} > {name2}')])
    plt.xticks(keys)

    plt.tight_layout()  # Prevent labels from overlapping
    plt.subplots_adjust(top=0.85)  # Adjust the top margin to make space for the title

    plt.savefig(f'results/graphs/{fig_name}')
    plt.close()

def generate_RoadGraph(file1, file2, type):
    data1 = cars_per_edge(file1)
    data2 = cars_per_edge(file2)

    with open('Adapters/co_simulation/road.json', 'r') as f:
        road_data = json.load(f)

    results_before = {road: 0 for road in road_data}
    results_after = {road: 0 for road in road_data}

    for road in road_data:
        road_edges = road_data[road]["edges"]
        for edge in road_edges:
            results_before[road] += data1[edge]
            results_after[road] += data2[edge]

    difference = {}
    for key in road_data:
        value1 = results_before[key]
        value2 = results_after[key]
        difference[key] = value2 - value1

    difference = {key: value for key, value in difference.items() if value != 0}
    keys = list(difference.keys())
    values = list(difference.values())

    colors = ['orange' if v > 0 else 'blue' for v in values]

    plt.figure(figsize=(10, 6))  # Increase the figure size

    plt.bar(keys, values, color=colors)
    plt.xlabel('Road Number')

    fig_name = ""
    name1 = file1.split("_edges")[0].split("/")[-1]
    name2 = file2.split("_edges")[0].split("/")[-1]

    total_cars1 = get_total_cars(file1.split("_edges")[0] + "_total_vehicles.json")
    total_cars2 = get_total_cars(file2.split("_edges")[0] + "_total_vehicles.json")
    total_time1 = get_total_time(file1.split("_edges")[0] + "_total_vehicles.json")
    total_time2 = get_total_time(file2.split("_edges")[0] + "_total_vehicles.json")

    if type == "co2":
        plt.ylabel('Average Difference in CO2 Emissions (mg)')
        plt.title(f'Average Difference in CO2 Emissions per road,\n {name2} ({total_cars2} vehicles in {total_time2} seconds) vs {name1} ({total_cars1} vehicles in {total_time1} seconds)')
        fig_name = f'RoadCO2_difference-{name1}-{name2}.png'

    elif type == "fuel":
        plt.ylabel('Average Difference in Fuel Consumption (ml)')
        plt.title(f'Average Difference in Fuel Consumption per road,\n {name2} ({total_cars2} vehicles in {total_time2} seconds) vs {name1} ({total_cars1} vehicles in {total_time1} seconds)')
        fig_name = f'RoadFuel_difference-{name1}-{name2}.png'

    elif type == "max":
        plt.ylabel('Difference in the Maximum Number of Vehicles')
        plt.title(f'Difference in the Maximum Number of Vehicles per road,\n {name2} ({total_cars2} vehicles in {total_time2} seconds) vs {name1} ({total_cars1} vehicles in {total_time1} seconds)')
        fig_name = f'RoadMax_difference-{name1}-{name2}.png'

    elif type == "total":
        plt.ylabel('Difference in the Total Number of Vehicles')
        plt.title(f'Difference in the Total Number of Vehicles per road,\n {name2} ({total_cars2} vehicles in {total_time2} seconds) vs {name1} ({total_cars1} vehicles in {total_time1} seconds)')
        fig_name = f'RoadTotal_difference-{name1}-{name2}.png'

    elif type == "waiting":
        plt.ylabel('Average Difference in the Accumulated Waiting Time (s)')
        plt.title(f'Average Difference in the Accumulated Waiting Time per road,\n {name2} ({total_cars2} vehicles in {total_time2} seconds) vs {name1} ({total_cars1} vehicles in {total_time1} seconds)')
        fig_name = f'RoadWaiting_difference-{name1}-{name2}.png'

    plt.legend(handles=[Patch(color='orange', label=f'{name2} > {name1}'), Patch(color='blue', label=f'{name1} > {name2}')])
    plt.xticks(rotation='vertical')  
    plt.tick_params(axis='x', labelsize=5)  
    plt.tight_layout()  
    plt.subplots_adjust(top=0.85)  # Adjust the top margin to make space for the title

    plt.savefig(f'results/graphs/{fig_name}')
    plt.close()

def generate_AllGraphs(sim1, sim2):
    file1_co2 = 'results/' + sim1 + "_edges_co2.json"
    file2_co2 = 'results/' + sim2 + "_edges_co2.json"
    file1_fuel = 'results/' + sim1 + "_edges_fuel.json"
    file2_fuel = 'results/' + sim2 + "_edges_fuel.json"
    file1_max = 'results/' + sim1 + "_edges_max.json"
    file2_max = 'results/' + sim2 + "_edges_max.json"
    file1_total = 'results/' + sim1 + "_edges_total.json"
    file2_total = 'results/' + sim2 + "_edges_total.json"
    file1_waiting = 'results/' + sim1 + "_edges_waiting.json"
    file2_waiting = 'results/' + sim2 + "_edges_waiting.json"

    files = [(file1_co2, file2_co2), (file1_fuel, file2_fuel), (file1_max, file2_max), (file1_total, file2_total), (file1_waiting, file2_waiting)]

    for file1, file2 in files:
        type = file1.split("_")[-1].split(".")[0]
        generate_RoadGraph(file1, file2, type)
        generate_RoundaboutGraph(file1, file2, type)

def get_total_cars(file):
    with open(file, 'r') as f:
        data = json.load(f)
    return data['total_vehicles']

def get_total_time(file):
    with open(file, 'r') as f:
        data = json.load(f)
    return data['total_time']

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 compare_traffic.py sim_name_1 sim_name_2")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]

    generate_AllGraphs(file1, file2)
