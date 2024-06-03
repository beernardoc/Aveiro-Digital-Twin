import sys
import json
import matplotlib.pyplot as plt

def cars_per_edge(file):
    with open(file, 'r') as f:
        data = json.load(f)

    # Excluir chaves que começam com ":"
    relevant_data = {key: value for key, value in data.items() if not key.startswith(':')}

    return relevant_data

def generate_RoundaboutGraph(file1, file2):
    data1 = cars_per_edge(file1)
    data2 = cars_per_edge(file2)

    with open('Adapters/co_simulation/roundabout.json', 'r') as f:
        roundabout_data = json.load(f)

    # Inicializar dicionários de resultados antes e depois
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

    # Removing keys with zero difference
    keys = list(difference.keys())
    values = list(difference.values())

    colors = ['orange' if v > 0 else 'blue' for v in values]

    # Ajuste a largura das barras
    bar_width = 0.5  # Defina a largura da barra conforme necessário

    plt.bar(keys, values, color=colors, width=bar_width)
    plt.xlabel('Roundabout')
    plt.ylabel('Difference in the Number of Cars')
    plt.title('Difference in the Number of Cars per roundabout')

    # Definindo os ticks do eixo x como os IDs das rotatórias
    plt.xticks(keys)

    plt.tight_layout()  # Prevent labels from overlapping

    plt.savefig('RoundAboutTraffic_difference.png')
    plt.close()




def generate_RoadGraph(file1, file2):
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

    # Removing keys with zero difference
    difference = {key: value for key, value in difference.items() if value != 0}
    keys = list(difference.keys())
    values = list(difference.values())

    colors = ['orange' if v > 0 else 'blue' for v in values]

    plt.bar(keys, values, color=colors)
    plt.xlabel('Road')
    plt.ylabel('Difference in the Number of Cars')
    plt.title('Difference in the Number of Cars per road')
    plt.xticks(rotation='vertical')  # Putting edge names vertically
    plt.tick_params(axis='x', labelsize=5)  # Reduce font size on x-axis labels
    plt.tight_layout()  # Prevent labels from overlapping

    plt.savefig('RoadTraffic_difference.png')
    plt.close()



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python program.py file1.json file2.json")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]

    generate_RoadGraph(file1, file2)
    generate_RoundaboutGraph(file1, file2)
