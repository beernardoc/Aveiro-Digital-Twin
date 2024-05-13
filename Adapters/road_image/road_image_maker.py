import cv2
import numpy as np
import json

# Load your image
image_path = 'road_image/base_road_image.png'
image = cv2.imread(image_path)

# Get the height of the image to adjust the y-coordinate
height, width = image.shape[:2]

# Define the array of points with original coordinates
with open('co_simulation/road.json') as f:
    all_roads = json.load(f)



# Adjust the y-coordinates to start from the bottom and convert to integer format
adjusted_roads = []
all_roads = dict(all_roads)
for road_id, road_points in all_roads.items():
    print(road_points)
    road_points = [(int(point[0]), int(point[1])) for point in road_points]
    adjusted_points = [(int(x), int(height - y)) for x, y in road_points]
    adjusted_roads.append(np.array(adjusted_points, dtype=np.int32))

# Define the color (BGR for red)
color = (0, 0, 255)

# Define the thickness of the line
thickness = 2

# Draw the lines on the image
for road in adjusted_roads:
    image = cv2.polylines(image, [road], isClosed=False, color=color, thickness=thickness)

# Display the image with lines
cv2.imshow('Image with Red Lines', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
