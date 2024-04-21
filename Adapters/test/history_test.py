import unittest
from history.file_composer import FileComposer

class TestFileComposer(unittest.TestCase):
    def setUp(self):
        self.file_composer = FileComposer('history/base_file.xml')

    def test_add_vehicle_tag(self):
        vehicle = {'id': '0', 'type': 'car', 'depart': '0'}
        self.file_composer.add_vehicle_tag(vehicle)

        self.assertEqual(self.file_composer.root[-1].tag, 'vehicle')
        self.assertEqual(self.file_composer.root[-1].attrib, vehicle)
        # inside the vehicle tag it should be empty
        self.assertEqual(len(self.file_composer.root[-1]), 0)

    def test_add_route_tag(self):
        # for a rouste to be added, the vehicle tag must be added first
        vehicle = {'id': '0', 'type': 'car', 'depart': '0'}
        self.file_composer.add_vehicle_tag(vehicle)

        route = ['-456', '-654', '-564']
        vehicle_id = '0'
        self.file_composer.add_route_tag(route, vehicle_id)

        self.assertEqual(self.file_composer.root[-1][0].tag, 'route')
        self.assertEqual(self.file_composer.root[-1][0].attrib, {'edges': '-456 -654 -564'})
        # make sure that the route was added to the correct vehicle
        self.assertEqual(self.file_composer.root[-1].attrib['id'], vehicle_id)

    def test_add_vehicle(self):
        vehicle = {'id': '0', 'type': 'test_car', 'depart': '0'}
        route = ['-123', '-321', '-231']
        self.file_composer.add_vehicle(vehicle, route)

        self.assertEqual(self.file_composer.root[1].tag, 'vehicle')
        self.assertEqual(self.file_composer.root[1].attrib, vehicle)
        self.assertEqual(self.file_composer.root[1][0].tag, 'route')
        self.assertEqual(self.file_composer.root[1][0].attrib, {'edges': '-123 -321 -231'})

    def test_add_vehicles(self):
        vehicles = [
            {'vehicle': {'id': '0', 'type': 'test_car', 'depart': '0'}, 'route': ['-123', '-321', '-231']},
            {'vehicle': {'id': '1', 'type': 'test_car', 'depart': '0'}, 'route': ['-456', '-654', '-564']}
        ]
        self.file_composer.add_vehicles(vehicles)

        # their shoud be 2 vehicles and 2 routes
        self.assertEqual(len(self.file_composer.root), 4)
        self.assertEqual(self.file_composer.root[1].tag, 'vehicle')
        self.assertEqual(self.file_composer.root[1].attrib, vehicles[0]['vehicle'])
        self.assertEqual(self.file_composer.root[1][0].tag, 'route')
        self.assertEqual(self.file_composer.root[1][0].attrib, {'edges': '-123 -321 -231'})
        self.assertEqual(self.file_composer.root[3].tag, 'vehicle')
        self.assertEqual(self.file_composer.root[3].attrib, vehicles[1]['vehicle'])
        self.assertEqual(self.file_composer.root[3][0].tag, 'route')
        self.assertEqual(self.file_composer.root[3][0].attrib, {'edges': '-456 -654 -564'})