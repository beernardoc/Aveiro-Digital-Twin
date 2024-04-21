import xml.etree.ElementTree as ET

class FileComposer:
    """
    Class that is responsible for composing a XML file that will be used
    as an history file for the simulation.
    If the user wants to store the simulation that can be used later on,
    a new XML file will be created with all the necessary information.
    """

    def __init__(self, base_file):
        self.base_file = base_file
        self.tree = ET.parse(self.base_file)
        self.root = self.tree.getroot()

    def add_vehicles(self, vehicles):
        """
        Add all the vehicles to the XML file.
        :param vehicles: A list with the vehicles information
        """

        for vehicle in vehicles:
            self.add_vehicle(vehicle['vehicle'], vehicle['route'])

    def add_vehicle(self, vehicle, route):
        """
        Add a vehicle to the XML file.
        :param vehicle: A map with the vehicle information (id, type, depart)
        :param route: A list with the edges that the vehicle will traverse
        """

        # Add the vehicle tag
        self.add_vehicle_tag(vehicle)

        # Add the route tag
        self.add_route_tag(route, vehicle['id'])

    def add_vehicle_tag(self, vehicle):
        """
        Add a vehicle tag to the XML file.
        :param vehicle: A map with the vehicle information (id, type, depart)
        """

        # Add a comment to the XML file
        self.add_comment(vehicle['id'], vehicle['type'], vehicle['depart'])

        # Create the vehicle tag
        new_vehicle = ET.Element('vehicle')

        # Add the vehicle attributes
        new_vehicle.set('id', vehicle['id'])
        new_vehicle.set('type', vehicle['type'])
        new_vehicle.set('depart', vehicle['depart'])

        # Insert the vehicle tag in the XML file
        self.root.insert(len(self.root), new_vehicle)

        # Save the changes
        self.save(self.base_file)

    def add_route_tag(self, route, vehicle_id):
        """
        Add a route tag to the XML file.
        :param route: A list with the edges that the vehicle will traverse
        :param vehicle_id: The vehicle id that will traverse the route
        """

        # Create the route tag
        new_route = ET.Element('route')

        # Add the route attributes
        new_route.set('edges', ' '.join(route))

        # Insert the route tag in the XML file
        for child in self.root:
            if child.tag == 'vehicle' and child.get('id') == vehicle_id:
                child.append(new_route)
                break

        # Save the changes
        self.save(self.base_file)

    def add_comment(self, id, type, depart):
        """
        Add a comment to the XML file.
        :param id: The vehicle id
        :param type: The vehicle type
        :param depart: The vehicle depart time
        """

        # Create the comment
        comment = f'Vehicle with id {id} and type {type} depart at {depart}'

        # Create the comment tag
        new_comment = ET.Comment(comment)

        # Insert the comment tag in the XML file
        self.root.insert(len(self.root), new_comment)

        # Save the changes
        self.save(self.base_file)

    def save(self, file_name):
        """
        Save the XML file with a new name.
        :param file_name: The new file name
        """

        self.tree.write(file_name, encoding='utf-8', xml_declaration=True)

# test if the class works
composer = FileComposer('base_file.xml')

vehicles = [
    {'vehicle': {'id': '0', 'type': 'test', 'depart': '0'}, 'route': ['-123', '-321', '-231']},
    {'vehicle': {'id': '1', 'type': 'test', 'depart': '0'}, 'route': ['-456', '-654', '-564']}
]

composer.add_vehicles(vehicles)