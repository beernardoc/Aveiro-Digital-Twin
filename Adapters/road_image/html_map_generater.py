import json

init_tag = '<map name="road">'
end_tag = '</map>'

base_polygon_tag = '<area shape="poly" coords="{}" alt="Road {}" style={{ cursor: "pointer" }} onClick={() => handleShow({})} />'

# get the roads from the json file
with open('co_simulation/road.json') as f:
    all_roads = json.load(f)

# output file
output_file = 'road_image/road_map.txt'

# write the initial tag
with open(output_file, 'w') as f:
    f.write(init_tag + '\n')

all_roads = dict(all_roads)

for road_id, road_points in all_roads.items():
    road_points_shape = [(int(point[0]), int(point[1])) for point in road_points['shape']]
    road_points_type = road_points['type']

    if road_points_type == 'polygon':
        road_points_shape = [f'{x},{y}' for x, y in road_points_shape]
        road_points_shape = ','.join(road_points_shape)
        tag = f'<area shape="poly" coords="{road_points_shape}" alt="Road {road_id}" style={{{{ cursor: "pointer" }}}} onClick={{() => handleShow("{road_id}")}} />'

        with open(output_file, 'a') as f:
            f.write('\t' + tag + '\n')

    else:
        # make a simple list of points
        road_points_shape = [x for point in road_points_shape for x in point]
        for i in range(0, len(road_points_shape) - 1):
            tag = f'<area shape="rect" coords="{road_points_shape[i]},{road_points_shape[i+1]}" alt="Road {road_id}" style={{{{ cursor: "pointer" }}}} onClick={{() => handleShow("{road_id}")}} />'
                
            with open(output_file, 'a') as f:
                f.write('\t' + tag + '\n')

# write the end tag
with open(output_file, 'a') as f:
    f.write(end_tag)

print(f'File {output_file} created')