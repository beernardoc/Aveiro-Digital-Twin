import pytest
from history.file_composer import FileComposer

@pytest.fixture
def file_composer():
    return FileComposer('history/base_file.xml')

def test_add_vehicle_tag(file_composer):
    vehicle = {'id': '0', 'type': 'car', 'depart': '0'}
    file_composer.add_vehicle_tag(vehicle)

    assert file_composer.root[-1].tag == 'vehicle'
    assert file_composer.root[-1].attrib == vehicle
    assert len(file_composer.root[-1]) == 0

def test_add_route_tag(file_composer):
    vehicle = {'id': '0', 'type': 'car', 'depart': '0'}
    file_composer.add_vehicle_tag(vehicle)

    route = ['-456', '-654', '-564']
    vehicle_id = '0'
    file_composer.add_route_tag(route, vehicle_id)

    assert file_composer.root[-1][0].tag == 'route'
    assert file_composer.root[-1][0].attrib == {'edges': '-456 -654 -564'}
    assert file_composer.root[-1].attrib['id'] == vehicle_id

def test_add_vehicle(file_composer):
    vehicle = {'id': '0', 'type': 'test_car', 'depart': '0'}
    route = ['-123', '-321', '-231']
    file_composer.add_vehicle(vehicle, route)

    assert file_composer.root[1].tag == 'vehicle'
    assert file_composer.root[1].attrib == vehicle
    assert file_composer.root[1][0].tag == 'route'
    assert file_composer.root[1][0].attrib == {'edges': '-123 -321 -231'}

def test_add_vehicles(file_composer):
    vehicles = [
        {'vehicle': {'id': '0', 'type': 'test_car', 'depart': '0'}, 'route': ['-123', '-321', '-231']},
        {'vehicle': {'id': '1', 'type': 'test_car', 'depart': '0'}, 'route': ['-456', '-654', '-564']}
    ]
    file_composer.add_vehicles(vehicles)

    assert len(file_composer.root) == 4
    assert file_composer.root[1].tag == 'vehicle'
    assert file_composer.root[1].attrib == vehicles[0]['vehicle']
    assert file_composer.root[1][0].tag == 'route'
    assert file_composer.root[1][0].attrib == {'edges': '-123 -321 -231'}
    assert file_composer.root[3].tag == 'vehicle'
    assert file_composer.root[3].attrib == vehicles[1]['vehicle']
    assert file_composer.root[3][0].tag == 'route'
    assert file_composer.root[3][0].attrib == {'edges': '-456 -654 -564'}