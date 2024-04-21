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