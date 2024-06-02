import sys
import json
import matplotlib.pyplot as plt

def cars_per_edge(file):
    with open(file, 'r') as f:
        data = json.load(f)
    return data

def generate_graph(file1, file2):
    data1 = cars_per_edge(file1)
    data2 = cars_per_edge(file2)

    keys = sorted(list(set(data1.keys()).union(set(data2.keys()))))  # Converting to list and sorting

    difference = {}
    for key in keys:
        value1 = data1.get(key, 0)
        value2 = data2.get(key, 0)
        difference[key] = value2 - value1

    # Removing keys with zero difference
    difference = {key: value for key, value in difference.items() if value != 0}

    keys = list(difference.keys())
    values = list(difference.values())

    colors = ['orange' if v > 0 else 'blue' for v in values]

    plt.bar(keys, values, color=colors)
    plt.xlabel('Edges')
    plt.ylabel('Difference in the Number of Cars')
    plt.title('Difference in the Number of Cars per Edge')
    plt.xticks(rotation='vertical')  # Putting edge names vertically
    plt.tick_params(axis='x', labelsize=4)  # Reduce font size on x-axis labels
    plt.tight_layout()  # Prevent labels from overlapping

    plt.savefig('traffic_difference.png')
    plt.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python program.py file1.json file2.json")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]

    generate_graph(file1, file2)
