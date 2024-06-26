import sumolib
import json

class Roads:
    def __init__(self, net_file):
        self.net = sumolib.net.readNet(net_file)
        self.roundabout_edges = []
        self.seen_edges = []
        self.roads = {}
        self.road_id = 1
        self.all_roads = {}

        # roundabout edges are inside the file roundabout.json
        with open('Adapters/co_simulation/roundabout.json') as f:
            data = json.load(f)
            
            for roundabout in data:
                for edge in roundabout['edges']:
                    self.roundabout_edges.append(edge)

        self.roundabout_edges = [str(edge) for edge in self.roundabout_edges]
    
    # method that given an edge id returns the other edge id that compose the road
    def get_adjacent_edges(self, edge_id):
        edge = self.net.getEdge(edge_id)
        from_node = edge.getFromNode()
        to_node = edge.getToNode()
        adjacent_edges = []

        for edge in from_node.getOutgoing():
            adjacent_edges.append(edge.getID())
        for edge in to_node.getOutgoing():
            adjacent_edges.append(edge.getID())

        return [edge for edge in adjacent_edges if edge != edge_id]
    
    def get_road(self, edge_id):
        edge = self.net.getEdge(edge_id)
        adjacent_edges = self.get_adjacent_edges(edge_id)
        from_node = edge.getFromNode().getID()
        to_node = edge.getToNode().getID()

        for adj_edge in adjacent_edges:
            adj_edge = self.net.getEdge(adj_edge)

            if adj_edge.getFromNode().getID() == to_node and adj_edge.getToNode().getID() == from_node:
                return [edge.getID(), adj_edge.getID()]
            
        return [edge.getID()]
            
    def get_roads(self):
        for edge in self.net.getEdges():
            edge_id = edge.getID()

            if edge.getType() == 'sidewalk' or edge.getLength() < 10:
                continue

            if edge_id not in self.seen_edges and edge_id not in self.roundabout_edges:
                road = self.get_road(edge_id)
                self.roads[self.road_id] = road
                
                
                for road_edge in road:
                    self.seen_edges.append(road_edge)
                    edge = self.net.getEdge(road_edge)
                    if self.road_id not in self.all_roads:
                        self.all_roads[self.road_id] = {'shape': edge.getShape(), 'type': 'line', 'edges': road}
                    else:
                        self.all_roads[self.road_id]['shape'] += edge.getShape()
                        self.all_roads[self.road_id]['type'] = 'polygon'
                        self.all_roads[self.road_id]['edges'] = road
                        print(f'{self.road_id}', self.all_roads[self.road_id])

                self.road_id += 1

    
if __name__ == '__main__':
    roads = Roads('Adapters/co_simulation/sumo_configuration/simple-map/UA.net.xml')
    roads.get_roads()
    
    # create a json file with the roads
    with open('Adapters/co_simulation/road.json', 'w') as f:
        json.dump(roads.all_roads, f)