import json
import cv2

init_tag = '<map name="road">'
end_tag = '</map>'

# get the roads from the json file
with open('Adapters/co_simulation/road.json') as f:
    all_roads = json.load(f)

# get the height of the image to adjust the y-coordinate
image_path = 'Adapters/road_image/base_road_image.png'
image = cv2.imread(image_path)

# Get the height of the image to adjust the y-coordinate
height, width = image.shape[:2]


# output file
output_file = 'Adapters/road_image/road_map.txt'

# write the initial tag
with open(output_file, 'w') as f:
    f.write(init_tag + '\n')

all_roads = dict(all_roads)

for road_id, road_points in all_roads.items():
    road_points_shape = [(int(point[0]), height - int(point[1])) for point in road_points['shape']]
    road_points_type = road_points['type']

    if road_points_type == 'polygon':
        road_points_shape = [f'{x},{y}' for x, y in road_points_shape]
        road_points_shape = ','.join(road_points_shape)
        tag = f'<area shape="poly" coords="{road_points_shape}" alt="Road {road_id}" style={{{{ cursor: "pointer" }}}} onClick={{() => handleShow("{road_id}")}} />'

        with open(output_file, 'a') as f:
            f.write('\t' + tag + '\n')

    else:
        # make a simple list of points
        road_points_shape = [(int(point[0]), height - int(point[1])) for point in road_points['shape']]
        for i in range(0, len(road_points_shape) - 1):
            tag = f'<area shape="rect" coords="{road_points_shape[i][0]}, {road_points_shape[i][1]}, {road_points_shape[i+1][0]}, {road_points_shape[i+1][1]}" alt="Road {road_id}" style={{{{ cursor: "pointer" }}}} onClick={{() => handleShow("{road_id}")}} />'
                
            with open(output_file, 'a') as f:
                f.write('\t' + tag + '\n')

# write the end tag
with open(output_file, 'a') as f:
    f.write(end_tag)

print(f'File {output_file} created')