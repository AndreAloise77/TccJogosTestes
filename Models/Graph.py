from typing import Dict, List

from Models.GraphVertex import GraphVertex
from Models.GraphEdge import GraphEdge


class Graph:
    def __init__(self):
        self.edges: Dict[str, GraphEdge] = {}
        self.vertices: Dict[str, GraphVertex] = {}
        self.newEdgeElements: List[str] = []
        self.newVertexElements: List[str] = []

    def add_edge(self, source_vertex_region: str, target_vertex_region: str, file_name: str):
        key_value = source_vertex_region + '_' + target_vertex_region
        if key_value in self.edges:
            edge = self.edges.get(key_value)
            edge.frequency += 1
            edge.sessions.append(file_name)
        else:
            source = self.__add_vertex(source_vertex_region, self.vertices)
            target = self.__add_vertex(target_vertex_region, self.vertices)
            edge = GraphEdge(source, target, file_name)
            self.edges[key_value] = edge
            self.newEdgeElements.append(key_value)

    def __add_vertex(self, region: str, dictionary_vertex: Dict[str, GraphVertex]):
        if not (region in dictionary_vertex):
            vertex = GraphVertex(region)
            dictionary_vertex[region] = vertex
            self.newVertexElements.append(region)
            return vertex
        else:
            return dictionary_vertex[region]

    def print_graph(self):
        for edge in self.edges:
            print('{}'.format(self.edges[edge].print_edge()))

    def get_edges(self):
        return self.edges

    def empty_lists(self):
        self.newEdgeElements = []
        self.newVertexElements = []

    def print_edge_list(self):
        print(self.newEdgeElements)
        print(self.newVertexElements)
