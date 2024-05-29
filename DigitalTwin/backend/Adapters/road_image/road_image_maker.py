import cv2
import numpy as np
import json

# Load your image
image_path = 'Adapters/road_image/base_road_image.png'
image = cv2.imread(image_path)

# Get the height of the image to adjust the y-coordinate
height, width = image.shape[:2]

# Define the array of points with original coordinates
with open('Adapters/co_simulation/road.json') as f:
    all_roads = json.load(f)



# Adjust the y-coordinates to start from the bottom and convert to integer format
adjusted_roads = []
adjusted_roads_type = []
all_roads = dict(all_roads)
for road_id, road_points in all_roads.items():
    road_points_shape = [(int(point[0]), int(point[1])) for point in road_points['shape']]
    adjusted_points = [(int(x), int(height - y)) for x, y in road_points_shape]
    adjusted_roads.append(np.array(adjusted_points, dtype=np.int32))
    adjusted_roads_type.append(road_points['type'])

# Define the color (BGR for red)
# dark purple
primary_color = (128, 0, 128)
second_color = (0, 0, 255)

# Define the thickness of the line
thickness = 2

# Draw the lines on the image
for i, road in enumerate(adjusted_roads):
    if i % 2 == 0:
        color = primary_color
    else:
        color = second_color


    if adjusted_roads_type[i] == 'line':
        image = cv2.polylines(image, [road], isClosed=False, color=color, thickness=thickness)
    else:
        image = cv2.fillPoly(image, [road], color=color)

# Display the image with lines
cv2.imshow('Image to put in the Frontend', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
# Save the image with lines
output_path = 'Adapters/road_image/image_roads_outlined.png'
cv2.imwrite(output_path, image)
print(f'Image saved in {output_path}')